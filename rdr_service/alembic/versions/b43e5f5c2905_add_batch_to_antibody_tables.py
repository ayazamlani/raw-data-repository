"""add batch to antibody tables

Revision ID: b43e5f5c2905
Revises: d28bd6bd0a8c
Create Date: 2020-10-20 16:58:53.619738

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
revision = 'b43e5f5c2905'
down_revision = 'd28bd6bd0a8c'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quest_covid_antibody_test', sa.Column('batch', sa.String(length=80), nullable=True))
    op.drop_index('accession', table_name='quest_covid_antibody_test')
    op.create_unique_constraint(None, 'quest_covid_antibody_test', ['accession', 'batch'])
    op.add_column('quest_covid_antibody_test_result', sa.Column('batch', sa.String(length=80), nullable=True))
    op.drop_index('accession', table_name='quest_covid_antibody_test_result')
    op.create_unique_constraint(None, 'quest_covid_antibody_test_result', ['accession', 'result_name', 'batch'])
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'quest_covid_antibody_test_result', type_='unique')
    op.create_index('accession', 'quest_covid_antibody_test_result', ['accession', 'result_name'], unique=True)
    op.drop_column('quest_covid_antibody_test_result', 'batch')
    op.drop_constraint(None, 'quest_covid_antibody_test', type_='unique')
    op.create_index('accession', 'quest_covid_antibody_test', ['accession'], unique=True)
    op.drop_column('quest_covid_antibody_test', 'batch')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
