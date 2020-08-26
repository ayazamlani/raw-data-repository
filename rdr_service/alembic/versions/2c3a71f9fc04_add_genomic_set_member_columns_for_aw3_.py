"""add_genomic_set_member columns_for_aw3_aw4

Revision ID: 2c3a71f9fc04
Revises: df7c40b6a209
Create Date: 2020-08-25 08:57:17.987756

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2c3a71f9fc04'
down_revision = 'df7c40b6a209'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_set_member', sa.Column('aw3_manifest_job_run_id', sa.Integer(), nullable=True))
    op.add_column('genomic_set_member_history', sa.Column('aw3_manifest_job_run_id', sa.Integer(), nullable=True))

    op.add_column('genomic_set_member', sa.Column('aw4_manifest_job_run_id', sa.Integer(), nullable=True))
    op.add_column('genomic_set_member_history', sa.Column('aw4_manifest_job_run_id', sa.Integer(), nullable=True))

    op.drop_constraint('genomic_set_member_ibfk_23', 'genomic_set_member', type_='foreignkey')
    op.drop_constraint('genomic_set_member_ibfk_24', 'genomic_set_member', type_='foreignkey')

    op.create_foreign_key(None, 'genomic_set_member', 'genomic_job_run', ['aw3_manifest_job_run_id'], ['id'])
    op.create_foreign_key(None, 'genomic_set_member', 'genomic_job_run', ['aw4_manifest_job_run_id'], ['id'])

    op.drop_column('genomic_set_member', 'wgs_aw3_manifest_job_run_id')
    op.drop_column('genomic_set_member_history', 'wgs_aw3_manifest_job_run_id')

    op.drop_column('genomic_set_member', 'arr_aw3_manifest_job_run_id')
    op.drop_column('genomic_set_member_history', 'arr_aw3_manifest_job_run_id')
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_set_member', sa.Column('arr_aw3_manifest_job_run_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('genomic_set_member_history', sa.Column('arr_aw3_manifest_job_run_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))

    op.add_column('genomic_set_member', sa.Column('wgs_aw3_manifest_job_run_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('genomic_set_member_history', sa.Column('wgs_aw3_manifest_job_run_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))

    op.drop_constraint(None, 'genomic_set_member', type_='foreignkey')
    op.drop_constraint(None, 'genomic_set_member', type_='foreignkey')

    op.create_foreign_key('genomic_set_member_ibfk_24', 'genomic_set_member', 'genomic_job_run', ['wgs_aw3_manifest_job_run_id'], ['id'])
    op.create_foreign_key('genomic_set_member_ibfk_23', 'genomic_set_member', 'genomic_job_run', ['arr_aw3_manifest_job_run_id'], ['id'])

    op.drop_column('genomic_set_member', 'aw4_manifest_job_run_id')
    op.drop_column('genomic_set_member_history', 'aw4_manifest_job_run_id')

    op.drop_column('genomic_set_member', 'aw3_manifest_job_run_id')
    op.drop_column('genomic_set_member_history', 'aw3_manifest_job_run_id')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

