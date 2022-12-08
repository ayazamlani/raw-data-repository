"""Update stored sample

Revision ID: 76d21e039dfd
Revises: b14e7aca2366
Create Date: 2017-09-08 16:22:39.521058

"""
import model.utils
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "76d21e039dfd"
down_revision = "b14e7aca2366"
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("biobank_stored_sample", sa.Column("created", model.utils.UTCDateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("biobank_stored_sample", "created")
    # ### end Alembic commands ###
