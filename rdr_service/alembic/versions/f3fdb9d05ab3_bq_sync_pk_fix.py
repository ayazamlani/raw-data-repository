"""bq_sync_pk_fix

Revision ID: f3fdb9d05ab3
Revises: 7d63fbc6d9ca
Create Date: 2019-08-14 12:10:16.423602

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
revision = 'f3fdb9d05ab3'
down_revision = '7d63fbc6d9ca'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    if engine_name == "rdr" or engine_name == "metrics":
        globals()[f"upgrade_{engine_name}"]()
    else:
        pass


def downgrade(engine_name):
    if engine_name == "rdr" or engine_name == "metrics":
        globals()[f"downgrade_{engine_name}"]()
    else:
        pass



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('TRUNCATE TABLE bigquery_sync')  # We want to start over now, these are some big changes.
    op.add_column('bigquery_sync', sa.Column('pk_id', sa.Integer(), nullable=False))
    op.execute('ALTER TABLE bigquery_sync ADD COLUMN `project_id` VARCHAR(80) NOT NULL AFTER modified')
    # op.add_column('bigquery_sync', sa.Column('project_id', sa.String(length=80), nullable=True))
    op.drop_constraint(u'bigquery_sync_ibfk_1', 'bigquery_sync', type_='foreignkey')
    op.drop_index('ix_participant_ds_table', table_name='bigquery_sync')
    op.execute('ALTER TABLE bigquery_sync CHANGE COLUMN `dataset` `dataset_id` VARCHAR(80) NOT NULL')
    op.execute('ALTER TABLE bigquery_sync CHANGE COLUMN `table` `table_id` VARCHAR(80) NOT NULL')
    op.create_index('ix_participant_ds_table', 'bigquery_sync', ['pk_id', 'project_id', 'dataset_id', 'table_id'], unique=False)
    op.drop_column('bigquery_sync', 'participant_id')
    # ### end Alembic commands ###
    pass

def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('TRUNCATE TABLE bigquery_sync')  # We want to start over now, these are some big changes.
    op.drop_index('ix_participant_ds_table', table_name='bigquery_sync')
    op.execute('ALTER TABLE bigquery_sync CHANGE COLUMN `dataset_id` `dataset` VARCHAR(80) NOT NULL')
    op.execute('ALTER TABLE bigquery_sync CHANGE COLUMN `table_id` `table` VARCHAR(80) NOT NULL')
    op.add_column('bigquery_sync',
                  sa.Column('participant_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_foreign_key(u'bigquery_sync_ibfk_1', 'bigquery_sync', 'participant', ['participant_id'],
                          ['participant_id'])
    op.create_index('ix_participant_ds_table', 'bigquery_sync', ['participant_id', 'dataset', 'table'], unique=False)
    op.drop_column('bigquery_sync', 'pk_id')
    op.drop_column('bigquery_sync', 'project_id')
    # ### end Alembic commands ###
    pass


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
