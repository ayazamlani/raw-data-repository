
from rdr_service import code_constants, participant_enums
from rdr_service.domain_model.response import Response
from rdr_service.logic.response.response_processor import ResponseProcessor
from rdr_service.model.participant_summary import ParticipantSummary


class EhrResponseProcessor(ResponseProcessor):
    def process_response(self, response: Response, summary: ParticipantSummary):
        if not self.is_response_to_relevant_survey(
            response,
            [code_constants.CONSENT_FOR_ELECTRONIC_HEALTH_RECORDS_MODULE]
        ):
            return False

        # Overwrites expiry
        if (
            summary.ehrConsentExpireStatus == participant_enums.ConsentExpireStatus.EXPIRED
            and response.authored_datetime > summary.ehrConsentExpireAuthored
        ):
            summary.ehrConsentExpireStatus = participant_enums.ConsentExpireStatus.UNSET
            summary.ehrConsentExpireAuthored = None
            summary.ehrConsentExpireTime = None

        new_status = participant_enums.QuestionnaireStatus.SUBMITTED_NO_CONSENT
        ehr_consent_answer = self.get_answer(response, code_constants.EHR_CONSENT_QUESTION_CODE)
        if ehr_consent_answer.value.lower() == code_constants.CONSENT_PERMISSION_YES_CODE.lower():
            # TODO: figure out what to do about consents

            new_status = participant_enums.QuestionnaireStatus.SUBMITTED

            if summary.consentForElectronicHealthRecordsFirstYesAuthored is None:
                summary.consentForElectronicHealthRecordsFirstYesAuthored = response.authored_datetime
            if (
                summary.ehrConsentExpireStatus == participant_enums.ConsentExpireStatus.EXPIRED
                and summary.ehrConsentExpireAuthored > response.authored_datetime
            ):
                new_status = participant_enums.QuestionnaireStatus.SUBMITTED_NO_CONSENT

        if (
            new_status != summary.consentForElectronicHealthRecords
            and (
                summary.consentForElectronicHealthRecordsAuthored is None
                or response.authored_datetime > summary.consentForElectronicHealthRecordsAuthored
            )
        ):
            summary.consentForElectronicHealthRecords = new_status
            summary.consentForElectronicHealthRecordsTime = response.created_datetime
            summary.consentForElectronicHealthRecordsAuthored = response.authored_datetime

            return True

        return False


        #  elif code.value in [EHR_CONSENT_QUESTION_CODE, EHR_SENSITIVE_CONSENT_QUESTION_CODE]:
        #     code = code_dao.get(answer.valueCodeId)
        #     if participant_summary.ehrConsentExpireStatus == ConsentExpireStatus.EXPIRED and \
        #             authored > participant_summary.ehrConsentExpireAuthored:
        #         participant_summary.ehrConsentExpireStatus = ConsentExpireStatus.UNSET
        #         participant_summary.ehrConsentExpireAuthored = None
        #         participant_summary.ehrConsentExpireTime = None
        #     if code and code.value in [CONSENT_PERMISSION_YES_CODE, SENSITIVE_EHR_YES]:
        #         self.consents_provided.append(ConsentType.EHR)
        #         ehr_consent = True
        #         if participant_summary.consentForElectronicHealthRecordsFirstYesAuthored is None:
        #             participant_summary.consentForElectronicHealthRecordsFirstYesAuthored = authored
        #         if participant_summary.ehrConsentExpireStatus == ConsentExpireStatus.EXPIRED and \
        #                 authored < participant_summary.ehrConsentExpireAuthored:
        #             ehr_consent = False
