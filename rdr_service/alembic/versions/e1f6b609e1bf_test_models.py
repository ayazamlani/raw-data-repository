"""test_models

Revision ID: e1f6b609e1bf
Revises: 57515daf8448, 33b34f5ae271
Create Date: 2022-03-28 11:20:19.570298

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
revision = 'e1f6b609e1bf'
down_revision = ('57515daf8448', '33b34f5ae271')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genomic_datagen_case_template',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('ignore_flag', sa.SmallInteger(), nullable=False),
    sa.Column('project_name', sa.String(length=255), nullable=False),
    sa.Column('template_name', sa.String(length=255), nullable=False),
    sa.Column('rdr_field', sa.String(length=255), nullable=False),
    sa.Column('field_source', sa.String(length=255), nullable=False),
    sa.Column('field_value', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genomic_datagen_output_template',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('ignore_flag', sa.SmallInteger(), nullable=False),
    sa.Column('project_name', sa.String(length=255), nullable=False),
    sa.Column('template_name', sa.String(length=255), nullable=False),
    sa.Column('field_index', sa.SmallInteger(), nullable=False),
    sa.Column('field_name', sa.String(length=255), nullable=False),
    sa.Column('source_type', sa.String(length=255), nullable=False),
    sa.Column('source_value', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genomic_datagen_run',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('ignore_flag', sa.SmallInteger(), nullable=False),
    sa.Column('project_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genomic_datagen_member_run',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('ignore_flag', sa.SmallInteger(), nullable=False),
    sa.Column('created_run_id', sa.Integer(), nullable=False),
    sa.Column('genomic_set_member_id', sa.Integer(), nullable=False),
    sa.Column('template_name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['created_run_id'], ['genomic_datagen_run.id'], ),
    sa.ForeignKeyConstraint(['genomic_set_member_id'], ['genomic_set_member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('genomic_datagen_member_run')
    op.drop_table('genomic_datagen_run')
    op.drop_table('genomic_datagen_output_template')
    op.drop_table('genomic_datagen_case_template')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

