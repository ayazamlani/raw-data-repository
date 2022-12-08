"""renaming Jan COPE to Feb

Revision ID: 942d61446bfa
Revises: 99fb6b79b5f7
Create Date: 2021-01-18 13:37:50.121134

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils
from sqlalchemy.dialects import mysql

from rdr_service.participant_enums import PhysicalMeasurementsStatus, QuestionnaireStatus, OrderStatus
from rdr_service.participant_enums import WithdrawalStatus, WithdrawalReason, SuspensionStatus, QuestionnaireDefinitionStatus
from rdr_service.participant_enums import EnrollmentStatus, Race, SampleStatus, OrganizationType, BiobankOrderStatus
from rdr_service.participant_enums import OrderShipmentTrackingStatus, OrderShipmentStatus
from rdr_service.participant_enums import MetricSetType, MetricsKey, GenderIdentity
from rdr_service.model.base import add_table_history_table, drop_table_history_table
from rdr_service.model.code import CodeType
from rdr_service.model.site_enums import SiteStatus, EnrollingStatus, DigitalSchedulingStatus, ObsoleteStatus

# revision identifiers, used by Alembic.
revision = '942d61446bfa'
down_revision = '99fb6b79b5f7'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant_summary', sa.Column('questionnaire_on_cope_feb', rdr_service.model.utils.Enum(QuestionnaireStatus), nullable=True))
    op.add_column('participant_summary', sa.Column('questionnaire_on_cope_feb_authored', rdr_service.model.utils.UTCDateTime(), nullable=True))
    op.add_column('participant_summary', sa.Column('questionnaire_on_cope_feb_time', rdr_service.model.utils.UTCDateTime(), nullable=True))
    op.drop_column('participant_summary', 'questionnaire_on_cope_jan_time')
    op.drop_column('participant_summary', 'questionnaire_on_cope_jan')
    op.drop_column('participant_summary', 'questionnaire_on_cope_jan_authored')
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant_summary', sa.Column('questionnaire_on_cope_jan_authored', mysql.DATETIME(), nullable=True))
    op.add_column('participant_summary', sa.Column('questionnaire_on_cope_jan', mysql.SMALLINT(display_width=6), autoincrement=False, nullable=True))
    op.add_column('participant_summary', sa.Column('questionnaire_on_cope_jan_time', mysql.DATETIME(), nullable=True))
    op.drop_column('participant_summary', 'questionnaire_on_cope_feb_time')
    op.drop_column('participant_summary', 'questionnaire_on_cope_feb_authored')
    op.drop_column('participant_summary', 'questionnaire_on_cope_feb')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
