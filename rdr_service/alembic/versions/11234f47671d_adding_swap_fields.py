"""adding_swap_fields

Revision ID: 11234f47671d
Revises: a3711bb1ef9d, d4bf2a726301, edf1adb41207
Create Date: 2022-08-16 15:44:21.368606

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '11234f47671d'
down_revision = ('a3711bb1ef9d', 'd4bf2a726301', 'edf1adb41207')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_sample_swap', sa.Column('description', sa.String(length=512), nullable=True))
    op.add_column('genomic_sample_swap', sa.Column('location', sa.String(length=512), nullable=True))
    op.add_column('genomic_sample_swap', sa.Column('number', sa.SmallInteger(), nullable=True))
    op.drop_column('genomic_sample_swap', 'explanation')
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_sample_swap', sa.Column('explanation', mysql.VARCHAR(length=512), nullable=True))
    op.drop_column('genomic_sample_swap', 'number')
    op.drop_column('genomic_sample_swap', 'location')
    op.drop_column('genomic_sample_swap', 'description')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
