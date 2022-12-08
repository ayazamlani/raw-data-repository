"""add irb to questionnaire

Revision ID: 90a21cce431b
Revises: 641372364227
Create Date: 2020-10-23 13:47:03.004003

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils


from rdr_service.participant_enums import PhysicalMeasurementsStatus, QuestionnaireStatus, OrderStatus
from rdr_service.participant_enums import WithdrawalStatus, WithdrawalReason, SuspensionStatus, QuestionnaireDefinitionStatus
from rdr_service.participant_enums import EnrollmentStatus, Race, SampleStatus, OrganizationType, BiobankOrderStatus
from rdr_service.participant_enums import OrderShipmentTrackingStatus, OrderShipmentStatus
from rdr_service.participant_enums import MetricSetType, MetricsKey, GenderIdentity
from rdr_service.model.base import add_table_history_table, drop_table_history_table
from rdr_service.model.code import CodeType
from rdr_service.model.site_enums import SiteStatus, EnrollingStatus, DigitalSchedulingStatus, ObsoleteStatus

# revision identifiers, used by Alembic.
revision = '90a21cce431b'
down_revision = '641372364227'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questionnaire', sa.Column('irb_mapping', sa.String(length=500), nullable=True))
    op.add_column('questionnaire', sa.Column('semantic_desc', sa.String(length=500), nullable=True))
    op.add_column('questionnaire_history', sa.Column('irb_mapping', sa.String(length=500), nullable=True))
    op.add_column('questionnaire_history', sa.Column('semantic_desc', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questionnaire_history', 'semantic_desc')
    op.drop_column('questionnaire_history', 'irb_mapping')
    op.drop_column('questionnaire', 'semantic_desc')
    op.drop_column('questionnaire', 'irb_mapping')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
