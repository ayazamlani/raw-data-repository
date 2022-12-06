"""add_saliva_code

Revision ID: f098d2c51614
Revises: e26ea978c345
Create Date: 2018-04-10 11:55:36.406746

"""
import model.utils
import sqlalchemy as sa
from alembic import op

from rdr_service.participant_enums import OrderStatus, SampleStatus

# revision identifiers, used by Alembic.
revision = "f098d2c51614"
down_revision = "e26ea978c345"
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
    op.add_column(
        "participant_summary", sa.Column("sample_order_status_1sal2", model.utils.Enum(OrderStatus), nullable=True)
    )
    op.add_column(
        "participant_summary", sa.Column("sample_order_status_1sal2_time", model.utils.UTCDateTime(), nullable=True)
    )
    op.add_column(
        "participant_summary", sa.Column("sample_status_1sal2", model.utils.Enum(SampleStatus), nullable=True)
    )
    op.add_column(
        "participant_summary", sa.Column("sample_status_1sal2_time", model.utils.UTCDateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("participant_summary", "sample_status_1sal2_time")
    op.drop_column("participant_summary", "sample_status_1sal2")
    op.drop_column("participant_summary", "sample_order_status_1sal2_time")
    op.drop_column("participant_summary", "sample_order_status_1sal2")
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
