"""add sample_source to aw2 raw

Revision ID: 93a39640573a
Revises: 73bce42825fa
Create Date: 2021-10-13 09:20:40.758459

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '93a39640573a'
down_revision = '73bce42825fa'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_aw2_raw', sa.Column('sample_source', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('genomic_aw2_raw', 'sample_source')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
