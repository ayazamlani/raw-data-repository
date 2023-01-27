import logging
from flask import request
from marshmallow import ValidationError

from rdr_service.api.base_api import UpdatableApi
from rdr_service.dao.study_nph_dao import NphIntakeDao
from rdr_service.api_util import RTI_AND_HEALTHPRO
from rdr_service.app_util import auth_required
from rdr_service.services.nph_intake_request_validation import IntakeApiSchema


class NphIntakeApi(UpdatableApi):

    def __init__(self):
        super(NphIntakeApi, self).__init__(NphIntakeDao)

    def update_with_patch(self, id_, resource, expected_version):
        pass

    @auth_required(RTI_AND_HEALTHPRO)
    def get(self):
        # resource = request.get_json(force=True)
        pass

    @auth_required(RTI_AND_HEALTHPRO)
    def post(self):
        resource = request.get_json(force=True)
        try:
            IntakeApiSchema().load(resource)
        except ValidationError as schema_error:
            logging.error(schema_error.messages)
            return schema_error.messages, 400

    @auth_required(RTI_AND_HEALTHPRO)
    def put(self):
        # resource = request.get_json(force=True)
        pass

