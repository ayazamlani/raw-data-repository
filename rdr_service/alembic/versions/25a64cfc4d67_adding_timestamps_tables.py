"""adding_timestamps_tables

Revision ID: 25a64cfc4d67
Revises: ee2270c92d0e
Create Date: 2022-01-25 10:15:51.132872

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
revision = '25a64cfc4d67'
down_revision = 'ee2270c92d0e'
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
    op.add_column('genomic_file_processed', sa.Column('created', rdr_service.model.utils.UTCDateTime(), nullable=True))
    op.add_column('genomic_file_processed', sa.Column('modified', rdr_service.model.utils.UTCDateTime(), nullable=True))
    op.add_column('genomic_job_run', sa.Column('created', rdr_service.model.utils.UTCDateTime(), nullable=True))
    op.add_column('genomic_job_run', sa.Column('modified', rdr_service.model.utils.UTCDateTime(), nullable=True))

    op.execute(
        """
        Update genomic_file_processed
        Set created = start_time,
            modified = end_time
        Where true
        and start_time is not null
        and end_time is not null
        """
    )

    op.execute(
        """
        Update genomic_job_run
        Set created = start_time,
            modified = end_time
        Where true
        and start_time is not null
        and end_time is not null
        """
    )

    op.execute(
        """
        INSERT INTO genomic_job_run (job_id, created, modified, start_time, end_time, run_status, run_result, job_id_str)
        VALUES (53, NOW(), NOW(), NOW(), NOW(), 1, 1, 'RECONCILE_PDR_DATA');
        """
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('genomic_job_run', 'modified')
    op.drop_column('genomic_job_run', 'created')
    op.drop_column('genomic_file_processed', 'modified')
    op.drop_column('genomic_file_processed', 'created')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
