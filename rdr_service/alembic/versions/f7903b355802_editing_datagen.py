"""editing_datagen

Revision ID: f7903b355802
Revises: 8e8e3911a2bd, a1b2e17c66ad
Create Date: 2022-04-19 10:11:41.707402

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f7903b355802'
down_revision = ('8e8e3911a2bd', 'a1b2e17c66ad')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genomic_datagen_case_template', 'created',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('genomic_datagen_case_template', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('genomic_datagen_manifest_schema', 'created',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('genomic_datagen_manifest_schema', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.add_column('genomic_datagen_member_run', sa.Column('end_to_end_start', sa.String(length=255), nullable=True))
    op.alter_column('genomic_datagen_member_run', 'created',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('genomic_datagen_member_run', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('genomic_datagen_output_template', 'created',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('genomic_datagen_output_template', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('genomic_datagen_run', 'created',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('genomic_datagen_run', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('genomic_datagen_run', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('genomic_datagen_run', 'created',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('genomic_datagen_output_template', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('genomic_datagen_output_template', 'created',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('genomic_datagen_member_run', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('genomic_datagen_member_run', 'created',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.drop_column('genomic_datagen_member_run', 'end_to_end_start')
    op.alter_column('genomic_datagen_manifest_schema', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('genomic_datagen_manifest_schema', 'created',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('genomic_datagen_case_template', 'modified',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('genomic_datagen_case_template', 'created',
               existing_type=mysql.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
