"""columns for dna consent update

Revision ID: c1198b53fdd6
Revises: ed465f72e410
Create Date: 2020-06-18 17:03:03.255362

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
revision = 'c1198b53fdd6'
down_revision = 'ed465f72e410'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant_summary', sa.Column('questionnaire_on_dna_program', rdr_service.model.utils.Enum(QuestionnaireStatus), nullable=True))
    op.add_column('participant_summary', sa.Column('questionnaire_on_dna_program_authored', rdr_service.model.utils.UTCDateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participant_summary', 'questionnaire_on_dna_program_authored')
    op.drop_column('participant_summary', 'questionnaire_on_dna_program')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
