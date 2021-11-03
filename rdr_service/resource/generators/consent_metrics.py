#
# This file is subject to the terms and conditions defined in the
# file 'LICENSE', which is part of this source code package.
#
import logging

from dateutil.relativedelta import relativedelta
from datetime import datetime, date

from rdr_service.dao.resource_dao import ResourceDataDao
from rdr_service.resource import generators, schemas
from rdr_service.model.consent_file import ConsentType, ConsentSyncStatus, ConsentFile, ConsentOtherErrors
from rdr_service.model.participant import Participant
from rdr_service.model.participant_summary import ParticipantSummary
from rdr_service.model.hpo import HPO
from rdr_service.model.organization import Organization

# Note:  Determination was made to treat a calculated age > 124 years at time of consent as an invalid DOB
# Currently must be 18 to consent to the AoU study.   These values could change in the future
INVALID_DOB_AGE_CUTOFF = 124
VALID_AGE_AT_CONSENT = 18
MISSING_SIGNATURE_FALSE_POSITIVE_CUTOFF_DATE = date(year=2018, month=7, day=13)

METRICS_ERROR_LIST = [
    'missing_file', 'invalid_signing_date', 'signature_missing', 'checkbox_unchecked', 'non_va_consent_for_va',
    'va_consent_for_non_va', 'invalid_dob', 'invalid_age_at_consent'
]

class ConsentMetricGenerator(generators.BaseGenerator):
    """
    Generate a ConsentMetric resource object
    """
    ro_dao = None

    @classmethod
    def _get_authored_timestamps_from_rec(cls, rec):
        """
        Find authored dates in the record (from participant_summary joined fields) based on consent type
        :param rec: A result row from ConsentMetricGenerator.get_consent_validation_records()
        :returns:  A dictionary of consent type keys and their authored date values from the result row
        """

        # Lower environments have some dirty/incomplete data (e.g., "FirstYesAuthored" fields were not backfilled)
        # Make a best effort to assign the appropriate authored date for a consent
        return {
            ConsentType.PRIMARY: rec.consentForStudyEnrollmentFirstYesAuthored\
                                 or rec.consentForStudyEnrollmentAuthored,
            ConsentType.EHR: rec.consentForElectronicHealthRecordsFirstYesAuthored\
                             or rec.consentForElectronicHealthRecordsAuthored,
            ConsentType.CABOR: rec.consentForCABoRAuthored,
            ConsentType.GROR: rec.consentForGenomicsRORAuthored,
            ConsentType.PRIMARY_UPDATE: rec.consentForStudyEnrollmentAuthored
        }

    def generate_error_text(self, consent_file_rec):
        """
        Create a textual error report from a ConsentMetric generator result.  This is used in
        reporting errors to PTSC via Jira
        :param consent_file_rec: A consent_file table row
        :return: A text string with the error details, or None if the generator data has the ignore flag set
        Example return string (formatted, without final newline chars):
            participant id:	P123456789
            consent type:	PRIMARY_UPDATE
            file path:	ptc-uploads-all-of-us-rdr-prod/Participant/P123456789/PrimaryConsentUpdate__8979.pdf
            file upload time:	2020-07-27 10:07:17
            Errors detected:	signature missing, non va consent for va
        """
        resource_data = self.make_resource(consent_file_rec.id).get_data()
        if resource_data['ignore']:
            return None

        # Need to include file details for PTSC error reports (vs. usual metrics reports)
        resource_data['file_path'] = consent_file_rec.file_path
        resource_data['file_upload_time'] = consent_file_rec.file_upload_time
        error_text = ''
        for field in ['participant_id', 'consent_type', 'file_path', 'file_upload_time']:
            error_text += f'{field.replace("_", " ")}:\t{resource_data[field]}\n'

        error_text += "Errors detected:\t"
        for error_flag_field in METRICS_ERROR_LIST:
            if resource_data[error_flag_field]:
                error_text += f'{error_flag_field.replace("_", " ")}, '

        # Replace trailing comma and space with newlines (for visual separation when this method is called iteratively)
        error_text = error_text[:-2] + "\n\n"
        return error_text

    def make_resource(self, _pk, consent_validation_rec=None):
        """
        Build a Resource object for the requested consent_file record
        :param _pk: Primary key id value from consent_file table
        :param consent_validation_rec:  A result row from get_consent_validation_records(), if one was already retrieved
        :return: ResourceDataObject object
        """
        if not self.ro_dao:
            self.ro_dao = ResourceDataDao(backup=True)

        if not consent_validation_rec:
            # Retrieve a single validation record for the provided id/primary key value
            result = self.get_consent_validation_records(id_list=[_pk])
            if not len(result):
                logging.warning(f'Consent metrics record retrieval failed for consent_file id {_pk}')
                return None
            else:
                consent_validation_rec = result[0]

        data = self._make_consent_validation_dict(consent_validation_rec)
        return generators.ResourceRecordSet(schemas.ConsentMetricSchema, data)

    @classmethod
    def has_errors(cls, resource_data, exclude=[]):
        """
        Confirms if the provided data dictionary as any error flags (other than the exclusions) set
        Convenience routine when filtering for false positives and want to look for error conditions other than
        the false positive error type
        :param resource_data:  data dictionary to check
        :param exclude: list of error keys to ignore/exclude from check
        """
        error_list = [e for e in METRICS_ERROR_LIST if e not in exclude]
        for error in error_list:
            if resource_data[error]:
                return True

        return False

    @staticmethod
    def _make_consent_validation_dict(row):
        """
        Transforms a result record from ConsentMetricGenerator.get_consent_validation_records() into a
        consent metrics resource object dictionary.  The content mirrors that of the pandas dataframe(s)
        generated by the tools/tool_libs/consent_validation_report.py manual spreadsheet report generator
        :param row: Result from get_consent_validation_records()
        """

        def _is_potential_false_positive_for_consent_version(resource, hpo):
            """
            In isolated cases, consent validation could run before a participant pairing to VA was complete, and could
            result in a potential false positive for va_consent_for_non_va errors.  This check returns True if:
                Status is NEEDS_CORRECTING
                Current pairing is to VA
                resource data dict has no other errors set besides va_consent_for_non_va
            """
            if (resource['sync_status'] != str(ConsentSyncStatus.NEEDS_CORRECTING)
                    or hpo != 'VA'
                    or ConsentMetricGenerator.has_errors(resource, exclude=['va_consent_for_non_va'])):
                return False

            return True

        def _is_potential_false_positive_for_missing_signature(resource, expected_sign_date, signing_date):
            """
            This identifies NEEDS_CORRECTING results that are known to be associated with false positives for
            missing signatures.  Returns True if all the following conditions exist:
                expected_sign_date < 2018-07-13 AND
                signing_date is null AND
                resource data dict has no other errors set besides signature_missing
            """
            if (resource['sync_status'] != str(ConsentSyncStatus.NEEDS_CORRECTING)
                    or signing_date
                    or (expected_sign_date and expected_sign_date >= MISSING_SIGNATURE_FALSE_POSITIVE_CUTOFF_DATE)
                    or ConsentMetricGenerator.has_errors(resource, exclude=['signature_missing'])):
                return False

            return True

        # -- MAIN BODY OF GENERATOR -- #
        if not row:
            raise (ValueError, 'Missing consent_file validation record')

        consent_type = row.type
        consent_status = row.sync_status

        # Set up default values
        data = {'id': row.id,
                'created': row.created,
                'modified': row.modified,
                'participant_id': f'P{row.participant_id}',
                'participant_origin': row.participantOrigin,
                'hpo': row.hpo_name,
                'hpo_id': row.hpoId,
                'organization': row.organization_name,
                'organization_id': row.organizationId,
                'consent_type': str(consent_type),
                'consent_type_id': int(consent_type),
                'sync_status': str(consent_status),
                'sync_status_id': int(consent_status),
                'consent_authored_date': None,
                'resolved_date': None,
                'missing_file': False,
                'signature_missing': False,
                'invalid_signing_date': False,
                'checkbox_unchecked': False,
                'non_va_consent_for_va': False,
                'va_consent_for_non_va': False,
                'invalid_dob': False,
                'invalid_age_at_consent': False,
                'test_participant': False,
                'ignore': False
        }

        # Look up the specific authored timestamp associated with this consent
        authored_ts_from_row = ConsentMetricGenerator._get_authored_timestamps_from_rec(row).get(consent_type, None)
        if authored_ts_from_row:
            data['consent_authored_date'] = authored_ts_from_row.date()

        # Resolved/OBSOLETE records use the consent_file modified date as the resolved date
        if consent_status == ConsentSyncStatus.OBSOLETE and row.modified:
            data['resolved_date'] = row.modified.date()

        # There is an implied hierarchy of some errors for metrics reporting.  Missing signature errors are not flagged
        # unless the file exists, and invalid signing date is not flagged unless there is a signature
        data['missing_file'] = not row.file_exists
        data['signature_missing'] = (row.file_exists and not row.is_signature_valid)
        data['invalid_signing_date'] = (row.is_signature_valid and not row.is_signing_date_valid)

        # Errors based on parsing the consent_file.other_errors string field:
        if row.other_errors:
            data['checkbox_unchecked'] =\
                row.other_errors.find(ConsentOtherErrors.MISSING_CONSENT_CHECK_MARK) != -1
            data['non_va_consent_for_va'] =\
                row.other_errors.find(ConsentOtherErrors.NON_VETERAN_CONSENT_FOR_VETERAN) != -1
            data['va_consent_for_non_va'] =\
                row.other_errors.find(ConsentOtherErrors.VETERAN_CONSENT_FOR_NON_VETERAN) != -1

        # DOB-related errors are not tracked in the RDR consent_file table.  They are derived from
        # participant_summary data and only apply to the primary consent.
        if consent_type == ConsentType.PRIMARY:
            dob = datetime(row.dateOfBirth.year,
                           row.dateOfBirth.month,
                           row.dateOfBirth.day) if row.dateOfBirth else None
            age_delta = relativedelta(authored_ts_from_row, dob) if dob else None
            data['invalid_dob'] = (dob is None
                                   or age_delta.years <= 0
                                   or age_delta.years >= INVALID_DOB_AGE_CUTOFF
                                   )
            data['invalid_age_at_consent'] = age_delta.years < VALID_AGE_AT_CONSENT if dob else False

        # PDR convention: map RDR ghost and test participants to test_participant = True
        data['test_participant'] = (row.hpo_name == 'TEST' or row.isTestParticipant == 1 or row.isGhostId == 1)

        # Special conditions where these records may be ignored for reporting.  Some known "false positive" conditions
        # or the record has a non-standard sync_status (LEGACY, UNKNOWN, DELAYING_SYNC),
        data['ignore'] = (_is_potential_false_positive_for_missing_signature(data,
                                                                             row.expected_sign_date,
                                                                             row.signing_date)
                          or _is_potential_false_positive_for_consent_version(data, row.hpo_name)
                          or row.sync_status > ConsentSyncStatus.SYNC_COMPLETE
                          )
        return data

    def get_consent_validation_records(self, dao=None, id_list=None, date_filter='2021-06-01'):
        """
        Retrieve a block of consent_file validation records based on an id list or  "modified since" date filter
        If an id list is provided, the date_filter will be ignored
        :param dao:  Read-only DAO object if one was already instantiated by the caller
        :param id_list: List of specific consent_file record IDs to retrieve.  Takes precedence over date_filter
        :param date_filter:  A date string in YYYY-MM-DD format to use for filtering consent_file records. The
                             default retrieves all records since consent validation started (in all environments)
        :return:  A result set from the query of consent validation data
        """
        if not dao:
            dao = self.ro_dao or ResourceDataDao(backup=True)

        with dao.session() as session:
            query = session.query(ConsentFile.id,
                                  ConsentFile.created,
                                  ConsentFile.modified,
                                  ConsentFile.participant_id,
                                  ConsentFile.type,
                                  ConsentFile.sync_status,
                                  ConsentFile.file_exists,
                                  ConsentFile.is_signature_valid,
                                  ConsentFile.is_signing_date_valid,
                                  ConsentFile.other_errors,
                                  ConsentFile.expected_sign_date,
                                  ConsentFile.signing_date,
                                  ParticipantSummary.dateOfBirth,
                                  ParticipantSummary.consentForStudyEnrollmentFirstYesAuthored,
                                  ParticipantSummary.consentForStudyEnrollmentAuthored,
                                  ParticipantSummary.consentForCABoRAuthored,
                                  ParticipantSummary.consentForElectronicHealthRecordsFirstYesAuthored,
                                  ParticipantSummary.consentForElectronicHealthRecordsAuthored,
                                  ParticipantSummary.consentForGenomicsRORAuthored,
                                  Participant.isGhostId,
                                  Participant.isTestParticipant,
                                  Participant.participantOrigin,
                                  HPO.hpoId,
                                  HPO.name.label('hpo_name'),
                                  Organization.organizationId,
                                  Organization.displayName.label('organization_name'))\
                  .join(ParticipantSummary, ParticipantSummary.participantId == ConsentFile.participant_id)\
                  .join(Participant, Participant.participantId == ConsentFile.participant_id)\
                  .outerjoin(HPO, HPO.hpoId == ParticipantSummary.hpoId)\
                  .outerjoin(Organization, ParticipantSummary.organizationId == Organization.organizationId)

            if id_list and len(id_list):
                query = query.filter(ConsentFile.id.in_(id_list))
            else:
                query = query.filter(ConsentFile.modified >= date_filter)

            results = query.all()
            if not results:
                logging.warning('No consent metrics results found.  Please check the query filters')

            return results
