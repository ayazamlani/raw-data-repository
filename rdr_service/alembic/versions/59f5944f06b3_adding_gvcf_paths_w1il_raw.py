"""adding_gvcf_paths_w1il_raw

Revision ID: 59f5944f06b3
Revises: 1acebc691c3c, 622c84ab202a
Create Date: 2022-06-27 16:24:57.213156

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '59f5944f06b3'
down_revision = ('1acebc691c3c', '622c84ab202a')
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genomic_w1il_raw', sa.Column('gvcf_md5_path', sa.String(length=255), nullable=True))
    op.add_column('genomic_w1il_raw', sa.Column('gvcf_path', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('genomic_w1il_raw', 'gvcf_path')
    op.drop_column('genomic_w1il_raw', 'gvcf_md5_path')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

