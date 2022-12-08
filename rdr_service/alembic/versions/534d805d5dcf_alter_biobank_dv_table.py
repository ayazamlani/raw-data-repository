"""alter biobank dv table

Revision ID: 534d805d5dcf
Revises: dc971fc16861
Create Date: 2019-03-18 13:23:40.194824

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "534d805d5dcf"
down_revision = "dc971fc16861"
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("biobank_dv_order", sa.Column("version", sa.Integer(), nullable=False))
    op.alter_column(
        "biobank_dv_order",
        "modified",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=False,
        existing_server_default=sa.text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"),
    )
    op.create_unique_constraint(None, "biobank_dv_order", ["biobank_order_id"])
    op.drop_column("biobank_dv_order", "biobank_reference")
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("biobank_dv_order", sa.Column("biobank_reference", mysql.VARCHAR(length=80), nullable=True))
    op.drop_constraint(None, "biobank_dv_order", type_="unique")
    op.alter_column(
        "biobank_dv_order",
        "modified",
        existing_type=mysql.DATETIME(fsp=6),
        nullable=True,
        existing_server_default=sa.text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"),
    )
    op.drop_column("biobank_dv_order", "version")
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
