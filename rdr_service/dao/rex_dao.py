from rdr_service.dao.base_dao import BaseDao
from rdr_service.model.rex import Study, ParticipantMapping


class RexStudyDao(BaseDao):

    def __init__(self):
        super().__init__(Study)

    def get_id(self, obj: Study):
        return obj.id

    def from_client_json(self):
        pass

    def get_prefix_by_schema(self, schema_name: str) -> tuple:
        with self.session() as session:
            return session.query(
                Study.prefix
            ).filter(
                Study.schema_name == schema_name
            ).first()


class RexParticipantMappingDao(BaseDao):

    def __init__(self):
        super().__init__(ParticipantMapping)

    def get_id(self, obj: ParticipantMapping):
        return obj.id

    def from_client_json(self):
        pass
