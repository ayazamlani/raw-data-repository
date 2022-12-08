"""add_columns_for_feedback_workflows

Revision ID: cab7fdee2895
Revises: 1b3c958942cb
Create Date: 2020-12-02 10:41:37.735608

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils
from rdr_service.genomic_enums import GenomicContaminationCategory

# revision identifiers, used by Alembic.
revision = 'cab7fdee2895'
down_revision = '1b3c958942cb'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_gc_validation_metrics', sa.Column('contamination_category',
                                                             rdr_service.model.utils.Enum(GenomicContaminationCategory),
                                                             nullable=True))
    op.add_column('genomic_manifest_feedback', sa.Column('ignore', sa.SmallInteger(), nullable=False))
    op.add_column('genomic_manifest_file', sa.Column('ignore', sa.SmallInteger(), nullable=False))

    op.create_unique_constraint('_file_path_ignore_uc', 'genomic_manifest_file', ['file_path', 'ignore'])

    op.add_column('genomic_set_member', sa.Column('aw1_file_processed_id', sa.Integer(), nullable=True))
    op.add_column('genomic_set_member_history', sa.Column('aw1_file_processed_id', sa.Integer(), nullable=True))

    op.add_column('genomic_set_member', sa.Column('aw2_file_processed_id', sa.Integer(), nullable=True))
    op.add_column('genomic_set_member_history', sa.Column('aw2_file_processed_id', sa.Integer(), nullable=True))

    op.add_column('genomic_set_member', sa.Column('aw2f_file_processed_id', sa.Integer(), nullable=True))
    op.add_column('genomic_set_member_history', sa.Column('aw2f_file_processed_id', sa.Integer(), nullable=True))

    op.create_foreign_key(None, 'genomic_set_member', 'genomic_file_processed', ['aw2_file_processed_id'], ['id'])
    op.create_foreign_key(None, 'genomic_set_member', 'genomic_file_processed', ['aw2f_file_processed_id'], ['id'])
    op.create_foreign_key(None, 'genomic_set_member', 'genomic_file_processed', ['aw1_file_processed_id'], ['id'])
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'genomic_set_member', type_='foreignkey')
    op.drop_constraint(None, 'genomic_set_member', type_='foreignkey')
    op.drop_constraint(None, 'genomic_set_member', type_='foreignkey')
    op.drop_column('genomic_set_member', 'aw2f_file_processed_id')
    op.drop_column('genomic_set_member_history', 'aw2f_file_processed_id')
    op.drop_column('genomic_set_member', 'aw2_file_processed_id')
    op.drop_column('genomic_set_member_history', 'aw2_file_processed_id')
    op.drop_column('genomic_set_member', 'aw1_file_processed_id')
    op.drop_column('genomic_set_member_history', 'aw1_file_processed_id')
    op.drop_constraint('_file_path_ignore_uc', 'genomic_manifest_file', type_='unique')
    op.drop_column('genomic_manifest_file', 'ignore')
    op.drop_column('genomic_manifest_feedback', 'ignore')
    op.drop_column('genomic_gc_validation_metrics', 'contamination_category')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
