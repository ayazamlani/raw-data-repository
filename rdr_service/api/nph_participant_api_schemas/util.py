from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, Dict
from graphene import List

from sqlalchemy.orm import Query, aliased
from rdr_service.model.participant_summary import ParticipantSummary as ParticipantSummaryModel
from rdr_service.participant_enums import QuestionnaireStatus


@dataclass
class QueryBuilder:
    query: Query
    order_expression: Optional = None
    filter_expressions: List = field(default_factory=list)
    references: Dict = field(default_factory=dict)
    join_expressions: List = field(default_factory=list)
    sort_table = None
    table = None

    def set_table(self, value):
        self.table = value

    def set_sort_table(self, reference):
        self.sort_table = self.references[reference]

    def add_filter(self, expr):
        self.filter_expressions.append(expr)

    def add_ref(self, table, ref_name):
        self.references[ref_name] = aliased(table)
        return self

    def add_join(self, joined_table, join_expr):
        self.join_expressions.append((joined_table, join_expr))
        return self

    def set_order_expression(self, expr):
        self.order_expression = expr

    def get_resulting_query(self):
        resulting_query = self.query

        for table, expr in self.join_expressions:
            resulting_query = resulting_query.join(table, expr)
        for expr in self.filter_expressions:
            resulting_query = resulting_query.filter(expr)

        return resulting_query.order_by(self.order_expression)


def check_field_value(value):
    if value is not None:
        return value
    return QuestionnaireStatus.UNSET


def load_participant_summary_data(query, prefix, biobank_prefix):
    results = []
    for summary, site, nph_site, mapping in query.all():
        results.append({
            'participantNphId': f"{prefix}{mapping.ancillary_participant_id}",
            'lastModified': summary.lastModified,
            'biobankId': f"{biobank_prefix}{summary.biobankId}",
            'firstName': summary.firstName,
            'middleName': summary.middleName,
            'lastName': summary.lastName,
            'dateOfBirth': summary.dateOfBirth,
            'zipCode': summary.zipCode,
            'phoneNumber': summary.phoneNumber,
            'email': summary.email,
            'deceasedStatus': {"value": check_field_value(summary.deceasedStatus),
                               "time": summary.deceasedAuthored},
            'withdrawalStatus': {"value": check_field_value(summary.withdrawalStatus),
                                 "time": summary.withdrawalAuthored},
            'nph_deactivation_status': {
                "value": QuestionnaireStatus.UNSET,
                "time": None
            },
            'nph_withdrawal_status': {
                "value": QuestionnaireStatus.UNSET,
                "time": None
            },
            'nph_enrollment_status': {"value": QuestionnaireStatus.UNSET,
                                      "time": None},
            'aianStatus': summary.aian,
            'suspensionStatus': {"value": check_field_value(summary.suspensionStatus),
                                 "time": summary.suspensionTime},
            'nphEnrollmentStatus': {"value": check_field_value(summary.enrollmentStatus),
                                 "time": summary.dateOfBirth},
            'questionnaireOnTheBasics': {
                "value": check_field_value(summary.questionnaireOnTheBasics),
                "time": summary.questionnaireOnTheBasicsAuthored
            },
            'questionnaireOnHealthcareAccess': {
                "value": check_field_value(summary.questionnaireOnHealthcareAccess),
                "time": summary.questionnaireOnHealthcareAccessAuthored
            },
            'questionnaireOnLifestyle': {
                "value": check_field_value(summary.questionnaireOnLifestyle),
                "time": summary.questionnaireOnLifestyleAuthored
            },
            'siteId': site.googleGroup,
            'external_id': nph_site.external_id,
            'organization_external_id': nph_site.organization_external_id,
            'awardee_external_id': nph_site.awardee_external_id,
            'questionnaireOnSocialDeterminantsOfHealth': {
                "value": check_field_value(summary.questionnaireOnSocialDeterminantsOfHealth),
                 "time": summary.questionnaireOnSocialDeterminantsOfHealthAuthored
            }
        })

    return results


def schema_field_lookup(value):
    try:
        field_lookup = {
            "DOB": {"field": "dateOfBirth", "table": ParticipantSummaryModel,
                    "value": ParticipantSummaryModel.dateOfBirth},
            "aouAianStatus": {"field": "aian", "table": ParticipantSummaryModel,
                              "value": ParticipantSummaryModel.aian},
            "aouBasicsStatus": {"field": "questionnaireOnTheBasics", "table": ParticipantSummaryModel,
                               "value": ParticipantSummaryModel.questionnaireOnTheBasics},
            "aouDeceasedStatus": {"field": "deceasedStatus", "table": ParticipantSummaryModel,
                                  "value": ParticipantSummaryModel.deceasedStatus,
                                  "time": ParticipantSummaryModel.deceasedAuthored},
            "aouWithdrawalStatus": {"field": "withdrawalStatus", "table": ParticipantSummaryModel,
                                    "value": ParticipantSummaryModel.withdrawalStatus,
                                    "time": ParticipantSummaryModel.withdrawalAuthored},
            "aouDeactivationStatus": {"field": "suspensionStatus", "table": ParticipantSummaryModel,
                                      "value": ParticipantSummaryModel.suspensionStatus,
                                      "time": ParticipantSummaryModel.suspensionTime},
            "aouEnrollmentStatus": {"field": "enrollmentStatus", "table": ParticipantSummaryModel,
                                    "value": ParticipantSummaryModel.enrollmentStatus,
                                    "time": ParticipantSummaryModel.enrollmentStatusParticipantV3_1Time},
            "aouOverallHealthStatus": {"field": "questionnaireOnHealthcareAccess", "table": ParticipantSummaryModel,
                                       "value": ParticipantSummaryModel.questionnaireOnHealthcareAccess,
                                       "time": ParticipantSummaryModel.questionnaireOnHealthcareAccessAuthored},
            "aouLifestyleStatus": {"field": "questionnaireOnLifestyle", "table": ParticipantSummaryModel,
                                   "value": ParticipantSummaryModel.questionnaireOnLifestyle,
                                   "time": ParticipantSummaryModel.questionnaireOnLifestyleAuthored},
            "aouSDOHStatus": {"field": "questionnaireOnSocialDeterminantsOfHealth", "table": ParticipantSummaryModel,
                              "value": ParticipantSummaryModel.questionnaireOnSocialDeterminantsOfHealth,
                              "time": ParticipantSummaryModel.questionnaireOnSocialDeterminantsOfHealthAuthored}
        }
        result = field_lookup.get(value)
        if result:
            return field_lookup.get(value)
        raise f"Invalid value : {value}"
    except KeyError as err:
        raise err


def load_participant_data(query):
    # query.session = sessions

    results = []
    for participants in query.all():
        samples_data = defaultdict(lambda: {
            'stored': {
                'parent': {
                    'current': None
                },
                'child': {
                    'current': None
                }
            }
        })
        for parent_sample in participants.samples:
            data_struct = samples_data[f'sample{parent_sample.test}']['stored']
            data_struct['parent']['current'] = {
                'value': parent_sample.status,
                'time': parent_sample.time
            }

            if len(parent_sample.children) == 1:
                child = parent_sample.children[0]
                data_struct['child']['current'] = {
                    'value': child.status,
                    'time': child.time
                }

        results.append(
            {
                'participantNphId': participants.participantId,
                'lastModified': participants.lastModified,
                'biobankId': participants.biobankId,
                **samples_data
            }
        )

    return []


def validation_error_message(errors):
    return {"errors": [error.formatted for error in errors]}


def error_message(message):
    return {"errors": message}
