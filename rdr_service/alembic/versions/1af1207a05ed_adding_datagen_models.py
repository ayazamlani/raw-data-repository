"""adding_datagen_models

Revision ID: 1af1207a05ed
Revises: 1d9563b9fab6
Create Date: 2022-04-04 12:21:17.116636

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1af1207a05ed'
down_revision = '1d9563b9fab6'
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
