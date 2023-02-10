import json
import logging
from flask import request
from marshmallow import ValidationError

from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy import exc

from rdr_service.api.base_api import UpdatableApi
from rdr_service.dao import database_factory
from rdr_service.dao.study_nph_dao import NphOrderDao, PatchUpdate, OrderObject
from rdr_service.api_util import RTI_AND_HEALTHPRO
from rdr_service.app_util import auth_required
from rdr_service.services.nph_biobank_order_payload_validation import (
    OrderSchema,
    RestoredUpdateSchema,
    CancelledUpdateSchema
)


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def construct_response(obj):
    # Construct Response payload
    return json.loads(json.dumps(obj, indent=4, cls=CustomEncoder))



class NphOrderApi(UpdatableApi):

    def __init__(self):
        super(NphOrderApi, self).__init__(NphOrderDao())

    def update_with_patch(self, id_, resource, expected_version):
        pass

    @auth_required(RTI_AND_HEALTHPRO)
    def put(self, nph_participant_id, rdr_order_id):
        try:
            if len(nph_participant_id) < 4:
                message = f"Invalid NPH Participant ID. Must be at least 5 characters in length. {nph_participant_id}"
                logging.error(message)
                return {"error": message}, 400
            with database_factory.get_database().session() as session:
                json_obj = request.get_json(force=True)
                OrderSchema().load(json_obj)
                order = OrderObject(json_obj)
                self.dao.validate(order, rdr_order_id, nph_participant_id, session)
                self.dao.order_sample_dao.update_order_sample(order, rdr_order_id, session)
                self.dao.update_order(order, rdr_order_id, nph_participant_id, session)
                json_obj["id"] = rdr_order_id
            return construct_response(json_obj), 201
        except NotFound as not_found:
            logging.error(not_found.description)
            return construct_response(json_obj), 404
        except BadRequest as bad_request:
            logging.error(bad_request.description)
            return construct_response(json_obj), 404
        except exc.SQLAlchemyError as sql:
            logging.error(sql)
            return construct_response(json_obj), 400

    @auth_required(RTI_AND_HEALTHPRO)
    def post(self, nph_participant_id: str):
        if len(nph_participant_id) < 4:
            message = f"Invalid NPH Participant ID. Must be at least 5 characters in length. {nph_participant_id}"
            logging.error(message)
            return {"error": message}, 400
        json_obj = request.get_json(force=True)
        try:
            OrderSchema().load(json_obj)
            obj = OrderObject(json_obj)
            with database_factory.get_database().session() as session:
                exist, time_point_id = self.dao.get_study_category_id(session, obj.study_category)
                if not exist:
                    logging.warning(f'Inserting new order to study_category table: '
                                    f'module = {obj.study_category.module}, '
                                    f'visitType: {obj.study_category.visit_type}, '
                                    f'timePoint: {obj.study_category.time_point}')
                    time_point_id = self.dao.insert_study_category_with_session(session, obj)[1]
                order = self.dao.from_client_json(session, nph_participant_id, time_point_id, obj)
                order = self.dao.insert_with_session(session, order)
                obj.set_id(order.id)
                self.dao.insert_ordered_sample_dao_with_session(session, obj)
                json_obj["id"] = order.id
                return construct_response(json_obj), 201
        except ValidationError as val_error:
            logging.error(val_error.messages)
            return val_error.messages, 400
        except NotFound as not_found:
            logging.error(not_found)
            return {"error": not_found}, 404
        except BadRequest as bad_request:
            logging.error(bad_request)
            return json_obj, 400
        except exc.SQLAlchemyError as sql:
            logging.error(sql)
            return json_obj, 400

    @auth_required(RTI_AND_HEALTHPRO)
    def patch(self, nph_participant_id, rdr_order_id):
        if len(nph_participant_id) < 4:
            message = f"Invalid NPH Participant ID. Must be at least 5 characters in length. {nph_participant_id}"
            logging.error(message)
            return {"error": message}, 400
        if rdr_order_id and nph_participant_id:
            json_obj = request.get_json(force=True)
            try:
                if json_obj["status"].upper() == "RESTORED":
                    RestoredUpdateSchema().load(json_obj)
                else:
                    CancelledUpdateSchema().load(json_obj)
                patch_update = PatchUpdate(json_obj)
                with database_factory.get_database().session() as session:
                    self.dao.patch_update(patch_update, rdr_order_id, nph_participant_id, session)
                    session.commit()
                    json_obj["id"] = rdr_order_id
                    return construct_response(json_obj), 200
            except ValidationError as val_error:
                logging.error(val_error.messages)
                return val_error.messages, 400
            except NotFound as not_found:
                logging.error(not_found.description)
                return construct_response(json_obj), 404
            except BadRequest as bad_request:
                logging.error(bad_request.description)
                return construct_response(json_obj), 400
            except exc.SQLAlchemyError as sql:
                logging.error(sql)
                return construct_response(json_obj), 400
