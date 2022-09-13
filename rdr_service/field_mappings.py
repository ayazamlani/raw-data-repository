"""Mappings from fields to question or module codes."""

from protorpc import messages

from rdr_service.code_constants import (
    CITY_QUESTION_CODE,
    CONSENT_FOR_DVEHR_MODULE,
    CONSENT_FOR_GENOMICS_ROR_MODULE,
    CONSENT_FOR_ELECTRONIC_HEALTH_RECORDS_MODULE,
    CONSENT_FOR_STUDY_ENROLLMENT_MODULE,
    DATE_OF_BIRTH_QUESTION_CODE,
    EDUCATION_QUESTION_CODE,
    EMAIL_QUESTION_CODE,
    FAMILY_HISTORY_MODULE,
    FIRST_NAME_QUESTION_CODE,
    GENDER_IDENTITY_QUESTION_CODE,
    HEALTHCARE_ACCESS_MODULE,
    INCOME_QUESTION_CODE,
    LANGUAGE_QUESTION_CODE,
    LAST_NAME_QUESTION_CODE,
    LIFESTYLE_PPI_MODULE,
    LOGIN_PHONE_NUMBER_QUESTION_CODE,
    MEDICATIONS_MODULE,
    MIDDLE_NAME_QUESTION_CODE,
    OVERALL_HEALTH_PPI_MODULE,
    PERSONAL_MEDICAL_HISTORY_MODULE,
    PHONE_NUMBER_QUESTION_CODE,
    RECONTACT_METHOD_QUESTION_CODE,
    SEXUAL_ORIENTATION_QUESTION_CODE,
    SEX_QUESTION_CODE,
    STATE_QUESTION_CODE,
    STREET_ADDRESS2_QUESTION_CODE,
    STREET_ADDRESS_QUESTION_CODE,
    THE_BASICS_PPI_MODULE,
    ZIPCODE_QUESTION_CODE,
    APPLE_EHR_SHARING_MODULE,
    APPLE_EHR_STOP_SHARING_MODULE,
    APPLE_HEALTH_KIT_SHARING_MODULE,
    APPLE_HEALTH_KIT_STOP_SHARING_MODULE,
    FITBIT_SHARING_MODULE,
    FITBIT_STOP_SHARING_MODULE,
    SOCIAL_DETERMINANTS_OF_HEALTH_MODULE,
    PERSONAL_AND_FAMILY_HEALTH_HISTORY_MODULE,
    LIFE_FUNCTIONING_SURVEY
)

# Field names for questionnaires / consent forms
CONSENT_FOR_STUDY_ENROLLMENT_FIELD = "consentForStudyEnrollment"
CONSENT_FOR_GENOMICS_ROR_FIELD = "consentForGenomicsROR"
CONSENT_FOR_ELECTRONIC_HEALTH_RECORDS_FIELD = "consentForElectronicHealthRecords"
QUESTIONNAIRE_ON_OVERALL_HEALTH_FIELD = "questionnaireOnOverallHealth"
QUESTIONNAIRE_ON_LIFESTYLE_FIELD = "questionnaireOnLifestyle"
QUESTIONNAIRE_ON_THE_BASICS_FIELD = "questionnaireOnTheBasics"
QUESTIONNAIRE_ON_MEDICAL_HISTORY_FIELD = "questionnaireOnMedicalHistory"
QUESTIONNAIRE_ON_MEDICATIONS_FIELD = "questionnaireOnMedications"
QUESTIONNAIRE_ON_FAMILY_HEALTH_FIELD = "questionnaireOnFamilyHealth"
QUESTIONNAIRE_ON_HEALTHCARE_ACCESS_FIELD = "questionnaireOnHealthcareAccess"
QUESTIONNAIRE_ON_DVEHR_SHARING_FIELD = "consentForDvElectronicHealthRecordsSharing"
QUESTIONNAIRE_ON_DIGITAL_HEALTH_SHARING_FIELD = "digitalHealthSharingStatus"
QUESTIONNAIRE_ON_SOCIAL_DETERMINANTS_OF_HEALTH = "questionnaireOnSocialDeterminantsOfHealth"
QUESTIONNAIRE_ON_PERSONAL_AND_FAMILY_HEALTH_HISTORY = "questionnaireOnPersonalAndFamilyHealthHistory"
QUESTIONNAIRE_ON_LIFE_FUNCTIONING = "questionnaireOnLifeFunctioning"


class FieldType(messages.Enum):
    """A type of field that shows up in a questionnaire response."""

    CODE = 1
    STRING = 2
    DATE = 3


FIELD_TO_QUESTION_CODE = {
    "genderIdentityId": (GENDER_IDENTITY_QUESTION_CODE, FieldType.CODE),
    "firstName": (FIRST_NAME_QUESTION_CODE, FieldType.STRING),
    "lastName": (LAST_NAME_QUESTION_CODE, FieldType.STRING),
    "middleName": (MIDDLE_NAME_QUESTION_CODE, FieldType.STRING),
    "streetAddress": (STREET_ADDRESS_QUESTION_CODE, FieldType.STRING),
    "streetAddress2": (STREET_ADDRESS2_QUESTION_CODE, FieldType.STRING),
    "city": (CITY_QUESTION_CODE, FieldType.STRING),
    "zipCode": (ZIPCODE_QUESTION_CODE, FieldType.STRING),
    "stateId": (STATE_QUESTION_CODE, FieldType.CODE),
    "phoneNumber": (PHONE_NUMBER_QUESTION_CODE, FieldType.STRING),
    "loginPhoneNumber": (LOGIN_PHONE_NUMBER_QUESTION_CODE, FieldType.STRING),
    "email": (EMAIL_QUESTION_CODE, FieldType.STRING),
    "recontactMethodId": (RECONTACT_METHOD_QUESTION_CODE, FieldType.CODE),
    "languageId": (LANGUAGE_QUESTION_CODE, FieldType.CODE),
    "sexId": (SEX_QUESTION_CODE, FieldType.CODE),
    "sexualOrientationId": (SEXUAL_ORIENTATION_QUESTION_CODE, FieldType.CODE),
    "educationId": (EDUCATION_QUESTION_CODE, FieldType.CODE),
    "incomeId": (INCOME_QUESTION_CODE, FieldType.CODE),
    "dateOfBirth": (DATE_OF_BIRTH_QUESTION_CODE, FieldType.DATE),
}
QUESTION_CODE_TO_FIELD = {v[0]: (k, v[1]) for k, v in list(FIELD_TO_QUESTION_CODE.items())}

FIELD_TO_QUESTIONNAIRE_MODULE_CODE = {
    # TODO: fill this in when correct codes are defined
    CONSENT_FOR_STUDY_ENROLLMENT_FIELD: CONSENT_FOR_STUDY_ENROLLMENT_MODULE,
    CONSENT_FOR_GENOMICS_ROR_FIELD: CONSENT_FOR_GENOMICS_ROR_MODULE,
    CONSENT_FOR_ELECTRONIC_HEALTH_RECORDS_FIELD: CONSENT_FOR_ELECTRONIC_HEALTH_RECORDS_MODULE,
    QUESTIONNAIRE_ON_OVERALL_HEALTH_FIELD: OVERALL_HEALTH_PPI_MODULE,
    QUESTIONNAIRE_ON_LIFESTYLE_FIELD: LIFESTYLE_PPI_MODULE,
    QUESTIONNAIRE_ON_THE_BASICS_FIELD: THE_BASICS_PPI_MODULE,
    QUESTIONNAIRE_ON_HEALTHCARE_ACCESS_FIELD: HEALTHCARE_ACCESS_MODULE,
    QUESTIONNAIRE_ON_MEDICAL_HISTORY_FIELD: PERSONAL_MEDICAL_HISTORY_MODULE,
    QUESTIONNAIRE_ON_MEDICATIONS_FIELD: MEDICATIONS_MODULE,
    QUESTIONNAIRE_ON_FAMILY_HEALTH_FIELD: FAMILY_HISTORY_MODULE,
    QUESTIONNAIRE_ON_SOCIAL_DETERMINANTS_OF_HEALTH: SOCIAL_DETERMINANTS_OF_HEALTH_MODULE,
    QUESTIONNAIRE_ON_PERSONAL_AND_FAMILY_HEALTH_HISTORY: PERSONAL_AND_FAMILY_HEALTH_HISTORY_MODULE,
    QUESTIONNAIRE_ON_DVEHR_SHARING_FIELD: CONSENT_FOR_DVEHR_MODULE,
    QUESTIONNAIRE_ON_LIFE_FUNCTIONING: LIFE_FUNCTIONING_SURVEY,
    QUESTIONNAIRE_ON_DIGITAL_HEALTH_SHARING_FIELD: [
        APPLE_EHR_SHARING_MODULE,
        APPLE_EHR_STOP_SHARING_MODULE,
        APPLE_HEALTH_KIT_SHARING_MODULE,
        APPLE_HEALTH_KIT_STOP_SHARING_MODULE,
        FITBIT_SHARING_MODULE,
        FITBIT_STOP_SHARING_MODULE
    ]
}

QUESTIONNAIRE_MODULE_CODE_TO_FIELD = {}
for k, v in list(FIELD_TO_QUESTIONNAIRE_MODULE_CODE.items()):
    if isinstance(v, str):
        QUESTIONNAIRE_MODULE_CODE_TO_FIELD[v] = k
    elif isinstance(v, list):
        for item in v:
            QUESTIONNAIRE_MODULE_CODE_TO_FIELD[item] = k

QUESTIONNAIRE_MODULE_FIELD_NAMES = sorted(FIELD_TO_QUESTIONNAIRE_MODULE_CODE.keys())
NON_EHR_QUESTIONNAIRE_MODULE_FIELD_NAMES = [
    field_name
    for field_name in QUESTIONNAIRE_MODULE_FIELD_NAMES
    if field_name != CONSENT_FOR_ELECTRONIC_HEALTH_RECORDS_FIELD
]
