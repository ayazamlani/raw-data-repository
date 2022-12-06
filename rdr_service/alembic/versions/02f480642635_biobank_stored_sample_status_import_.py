"""biobank stored sample status import temp table

Revision ID: 02f480642635
Revises: ebb897e84b1b
Create Date: 2020-12-07 12:51:12.215106

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils

# revision identifiers, used by Alembic.
revision = '02f480642635'
down_revision = 'ebb897e84b1b'
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
    op.create_table('biobank_stored_sample_status_import_tmp',
    sa.Column('sample_family_id', sa.String(length=80), nullable=True),
    sa.Column('sample_id', sa.String(length=80), nullable=True),
    sa.Column('sample_storage_status', sa.String(length=80), nullable=True),
    sa.Column('sample_type', sa.String(length=80), nullable=True),
    sa.Column('parent_expected_volume', sa.String(length=80), nullable=True),
    sa.Column('sample_quantity', sa.String(length=80), nullable=True),
    sa.Column('sample_container_type', sa.String(length=80), nullable=True),
    sa.Column('sample_family_collection_date', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('sample_disposal_status', sa.String(length=80), nullable=True),
    sa.Column('sample_disposed_date', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('parent_sample_id', sa.String(length=80), nullable=True),
    sa.Column('sample_confirmed_date', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('external_participant_id', sa.String(length=80), nullable=True),
    sa.Column('test_code', sa.String(length=80), nullable=True),
    sa.Column('sample_treatment', sa.String(length=80), nullable=True),
    sa.Column('sample_family_create_date', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('sent_order_id', sa.String(length=80), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_biobank_stored_sample_status_import_tmp_external_participant_id'), 'biobank_stored_sample_status_import_tmp', ['external_participant_id'], unique=False)
    op.create_index(op.f('ix_biobank_stored_sample_status_import_tmp_sample_id'), 'biobank_stored_sample_status_import_tmp', ['sample_id'], unique=False)
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_biobank_stored_sample_status_import_tmp_sample_id'), table_name='biobank_stored_sample_status_import_tmp')
    op.drop_index(op.f('ix_biobank_stored_sample_status_import_tmp_external_participant_id'), table_name='biobank_stored_sample_status_import_tmp')
    op.drop_table('biobank_stored_sample_status_import_tmp')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
