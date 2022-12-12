"""Initial metrics

Revision ID: 6f9266e7a5fb
Revises: 51415576d3e9
Create Date: 2017-12-12 10:38:27.166562

"""
import model.utils
import sqlalchemy as sa
from alembic import op

from rdr_service.participant_enums import MetricSetType, MetricsKey

# revision identifiers, used by Alembic.
revision = "6f9266e7a5fb"
down_revision = "51415576d3e9"
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "metric_set",
        sa.Column("metric_set_id", sa.String(length=50), nullable=False),
        sa.Column("metric_set_type", model.utils.Enum(MetricSetType), nullable=False),
        sa.Column("last_modified", model.utils.UTCDateTime(), nullable=False),
        sa.PrimaryKeyConstraint("metric_set_id"),
        schema="metrics",
    )
    op.create_table(
        "aggregate_metrics",
        sa.Column("metric_set_id", sa.String(length=50), nullable=False),
        sa.Column("metrics_key", model.utils.Enum(MetricsKey), nullable=False),
        sa.Column("value", sa.String(length=50), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["metric_set_id"], ["metrics.metric_set.metric_set_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("metric_set_id", "metrics_key", "value"),
        schema="metrics",
    )
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("aggregate_metrics", schema="metrics")
    op.drop_table("metric_set", schema="metrics")
    # ### end Alembic commands ###
