from dataclasses import dataclass

from flask import request
from werkzeug.exceptions import BadRequest

from rdr_service import clock
from rdr_service.api.base_api import BaseApi, log_api_request
from rdr_service.api_util import RTI, RDR
from rdr_service.app_util import auth_required
from rdr_service.dao.rex_dao import RexStudyDao
from rdr_service.dao.study_nph_dao import NphIntakeDao, NphParticipantEventActivityDao, NphActivityDao, \
    NphPairingEventDao, NphSiteDao, NphDefaultBaseDao, NphEnrollmentEventTypeDao
from rdr_service.model.study_nph import WithdrawalEvent, DeactivatedEvent, ConsentEvent, EnrollmentEvent


@dataclass
class ActivityData:
    id: int
    name: str
    source: str


class NphIntakeAPI(BaseApi):
    def __init__(self):
        super().__init__(NphIntakeDao())

        self.nph_prefix = RexStudyDao().get_prefix_by_schema('nph')
        self.nph_prefix = self.nph_prefix[0]

        self.current_activities = NphActivityDao().get_all()

        self.nph_participant_activity_dao = NphParticipantEventActivityDao()
        self.nph_site_dao = NphSiteDao()

        self.nph_enrollment_type_dao = NphEnrollmentEventTypeDao()

        self.nph_pairing_event_dao = NphPairingEventDao()
        self.nph_consent_event_dao = NphDefaultBaseDao(model_type=ConsentEvent)
        self.nph_enrollment_event_dao = NphDefaultBaseDao(model_type=EnrollmentEvent)
        self.nph_withdrawal_event_dao = NphDefaultBaseDao(model_type=WithdrawalEvent)
        self.nph_deactivation_event_dao = NphDefaultBaseDao(model_type=DeactivatedEvent)

        self.bundle_identifier = None

    def extract_activity_data(self, entry: dict):
        activity_name, activity_source = None, None

        try:
            activity_name = entry['resource']['resourceType']

            if entry['resource'].get('class'):
                activity_name = activity_source = entry['resource']['class']['code']

                if 'module' in activity_name:
                    activity_name = 'enrollment'

            if entry['resource'].get('serviceType'):
                activity_source = entry['resource']['serviceType']['coding'][0]['code']

            activity_name = activity_name.lower()
            current_activity = list(filter(lambda x: x.name.lower() == activity_name,
                                           self.current_activities))
            if not current_activity:
                raise BadRequest(f'Cannot reconcile activity type bundle_id: {self.bundle_identifier}')

            return ActivityData(
                id=current_activity[0].id,
                name=activity_name,
                source=activity_source
            )

        except KeyError as e:
            return BadRequest(f'Key error on activity lookup: {e} bundle_id: {self.bundle_identifier}')

    def get_site_id(self, entry: dict):
        try:
            pairing_site_code = entry['resource']['type'][0]['coding'][0]['code']

            if not pairing_site_code:
                raise BadRequest(f'Cannot find site pairing code: bundle_id: {self.bundle_identifier}')

            site = self.nph_site_dao.get_site_id_from_external(external_id=pairing_site_code)

            if not site:
                raise BadRequest(f'Cannot find site from site code: bundle_id: {self.bundle_identifier}')

            return site.id

        except KeyError as e:
            raise BadRequest(f'Key error on site lookup: {e} bundle_id: {self.bundle_identifier}')

    def get_event_type_id(self, *, activity_name, activity_source):
        event_type_dao_instance_items = {k: v for k, v in self.__dict__.items() if 'type_dao' in k}

        if activity_name not in event_type_dao_instance_items.keys():
            return 1

        event_type_dao = event_type_dao_instance_items[f'nph_{activity_name}_type_dao']
        event_activity = event_type_dao.get_event_by_source_name(source_name=activity_source)

        if not event_activity:
            raise BadRequest(f'Cannot find event type: bundle_id: {self.bundle_identifier}')

        return event_activity.id

    def build_event_dao_map(self):
        event_dao_map = {}
        event_dao_instance_items = {k: v for k, v in self.__dict__.items() if 'event_dao' in k}
        for activity in self.current_activities:
            event_dao_map[f'{activity.name.lower()}'] = event_dao_instance_items[
                f'nph_{activity.name.lower()}_event_dao']
        return event_dao_map

    def extract_participant_id(self, participant_obj: dict) -> str:
        participant_id = participant_obj['resource']['identifier'][0]['value']
        participant_id = participant_id.split(f'/{self.nph_prefix}')[-1]
        return participant_id

    def extract_authored_time(self, entry: dict):
        try:
            date_time = entry['resource'].get('dateTime')

            if not date_time and entry['resource'].get('period'):
                date_time = entry['resource']['period']['start']

            if not date_time:
                raise BadRequest(f'Cannot get value on authored time lookup bundle_id: {self.bundle_identifier}')

            return date_time

        except KeyError as e:
            raise BadRequest(f'KeyError on authored time lookup: {e} bundle_id: {self.bundle_identifier}')

    @auth_required([RTI, RDR])
    def post(self):
        intake_payload = request.get_json(force=True)
        intake_payload = [intake_payload] if type(intake_payload) is not list else intake_payload

        # Adding request log here so if exception is raised
        # per validation fail the payload is stored
        log_api_request(log=request.log_record)

        event_dao_map = self.build_event_dao_map()
        participant_event_objs, event_objs = [], []

        participant_response = []
        for resource in intake_payload:
            self.bundle_identifier = resource['identifier']['value']

            participant_obj = list(filter(lambda x: x['resource']['resourceType'].lower() == 'patient',
                                          resource['entry']))[0]

            participant_id = self.extract_participant_id(participant_obj=participant_obj)

            participant_response.append({
                'nph_participant_id': participant_id
            })

            applicable_entries = [obj for obj in resource['entry'] if obj['resource']['resourceType'].lower() in [
                'consent', 'encounter']]

            for entry in applicable_entries:

                activity_data = self.extract_activity_data(entry)
                entry['bundle_identifier'] = self.bundle_identifier

                participant_event_objs.append({
                    'created': clock.CLOCK.now(),
                    'modified': clock.CLOCK.now(),
                    'participant_id': participant_id,
                    'activity_id': activity_data.id,
                    'resource': entry
                })

                nph_event_dao = event_dao_map[activity_data.name]

                event_obj = {
                    'created': clock.CLOCK.now(),
                    'modified': clock.CLOCK.now(),
                    'event_authored_time': self.extract_authored_time(entry),
                    'participant_id': participant_id,
                    'additional': {
                        'nph_event_dao': nph_event_dao,
                        'activity_id': activity_data.id,
                        'bundle_identifier': self.bundle_identifier
                    }
                }

                if hasattr(nph_event_dao.model_type.__table__.columns, 'site_id'):
                    event_obj['site_id'] = self.get_site_id(entry)

                if hasattr(nph_event_dao.model_type.__table__.columns, 'event_type_id'):
                    event_obj['event_type_id'] = self.get_event_type_id(
                        activity_name=activity_data.name,
                        activity_source=activity_data.source
                    )

                event_objs.append(event_obj)

        self.nph_participant_activity_dao.insert_bulk(participant_event_objs)

        for dao_key, dao in event_dao_map.items():
            dao_event_objs = list(filter(
                lambda x: x.get('additional') and dao_key in x['additional'][
                    'nph_event_dao'].model_type.__name__.lower(), event_objs
            ))
            for dao_obj in dao_event_objs:
                participant_event_obj = self.nph_participant_activity_dao.get_activity_event_intake(
                    participant_id=dao_obj['participant_id'],
                    resource_identifier=dao_obj['additional']['bundle_identifier'],
                    activity_id=dao_obj['additional']['activity_id']
                )
                dao_obj['event_id'] = participant_event_obj.id
                del dao_obj['additional']

            if dao_event_objs:
                dao.insert_bulk(dao_event_objs)

        return self._make_response(participant_response)
