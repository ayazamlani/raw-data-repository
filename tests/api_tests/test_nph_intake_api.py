import json
# from datetime import datetime

from rdr_service.data_gen.generators.nph import NphDataGenerator
from tests.helpers.unittest_base import BaseTestCase
from tests.test_data import data_path


class NphIntakeAPITest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.nph_data_gen = NphDataGenerator()
        activities = ['ENROLLMENT', 'PAIRING', 'CONSENT', 'WITHDRAWAL', 'DEACTIVATION']

        for activity in activities:
            self.nph_data_gen.create_database_activity(
                name=activity
            )
        self.nph_data_gen.create_database_consent_event_type(
            name='Module 1',
            source_name='module1'
        )
        self.nph_data_gen.create_database_pairing_event_type(
            name="INITIAL"
        )
        self.nph_data_gen.create_database_enrollment_event_type(
            name="Module 1 Eligibility Confirmed",
            source_name='eligibilityConfirmed'
        )
        self.nph_data_gen.create_database_enrollment_event_type(
            name="Module 1 Consented",
            source_name='consented'
        )
        for _ in range(2):
            self.nph_data_gen.create_database_participant()

        for i in range(1, 3):
            self.nph_data_gen.create_database_site(
                external_id=f"nph-test-site-{i}",
                name=f"nph-test-site-name-{i}",
                awardee_external_id="nph-test-hpo",
                organization_external_id="nph-test-org"
            )

    def test_m1_detailed_consent_payload(self):

        with open(data_path('nph_m1_detailed_consent_multi.json')) as f:
            consent_json = json.load(f)

        self.send_post('nph/Intake', request_data=consent_json)

    def test_m1_operational_payload(self):

        with open(data_path('nph_m1_operational_multi.json')) as f:
            consent_json = json.load(f)

        self.send_post('nph/Intake', request_data=consent_json)

    def test_m2_operational_payload(self):

        with open(data_path('nph_m2_operational_multi.json')) as f:
            consent_json = json.load(f)

        self.send_post('nph/Intake', request_data=consent_json)

    def tearDown(self):
        super().tearDown()
        self.clear_table_after_test("nph.participant")
