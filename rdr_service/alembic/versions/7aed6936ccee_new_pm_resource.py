"""new pm resource

Revision ID: 7aed6936ccee
Revises: 7aad615d6979
Create Date: 2020-01-29 08:51:35.381339

"""
from alembic import op
import sqlalchemy as sa
import model.utils
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
revision = '7aed6936ccee'
down_revision = '7aad615d6979'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    # Prepare old resource column for migration.
    op.alter_column('physical_measurements', 'resource', existing_type=mysql.LONGBLOB(), nullable=True)
    op.execute('ALTER TABLE physical_measurements CHANGE `resource` `old_resource` longblob')
    # Add new resource column and populate it with the converted fhir docs.
    op.add_column('physical_measurements', sa.Column('resource', mysql.JSON(), nullable=True))
    op.execute('UPDATE physical_measurements SET resource = CAST(old_resource AS CHAR(120000) CHARACTER SET utf8)')
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('physical_measurements', 'resource')
    op.execute('ALTER TABLE physical_measurements CHANGE `old_resource` `resource` longblob')
    op.alter_column('physical_measurements', 'resource', existing_type=mysql.LONGBLOB(), nullable=False)
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
