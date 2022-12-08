"""add

Revision ID: d81ae8ae32ea
Revises: fc1eb86aa8f4, 355854d777d3
Create Date: 2021-06-25 11:54:54.415110

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
revision = 'd81ae8ae32ea'
down_revision = ('fc1eb86aa8f4', '355854d777d3')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genomic_informing_loop',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message_record_id', sa.Integer(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('event_type', sa.String(length=256), nullable=False),
    sa.Column('event_authored_time', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=True),
    sa.Column('module_type', sa.String(length=128), nullable=True),
    sa.Column('decision_value', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.participant_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genomic_informing_loop')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
