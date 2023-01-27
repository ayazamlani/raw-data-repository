import json
from marshmallow import ValidationError
from contextlib import contextmanager

from tests.helpers.unittest_base import BaseTestCase
from rdr_service.main import app
from rdr_service.services.nph_intake_request_validation import IntakeApiSchema


class TestNPHParticipantOrderAPI(BaseTestCase):

    @contextmanager
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type:
            raise self.failureException('{} raised'.format(exc_type.__name__))

    def test_intake_schema_validation(self):
        with open('tests/api_tests/nph/sample.json', 'r') as f:
            json_data = json.loads(f.read())
            with self.assertNotRaises(ValidationError):
                IntakeApiSchema().load(json_data)


    def test_post(self):
        json_data = {}
        executed = app.test_client().post('rdr/v1/api/v1/nph/Participant/1000124820391/BiobankOrder', json=json_data)
        result = json.loads(executed.data.decode('utf-8'))
        for k, _ in result.items():
            if k.upper() != "ID":
                self.assertEqual(json_data.get(k), result.get(k))

