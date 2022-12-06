"""Add physical measurement cols

Revision ID: b14e7aca2366
Revises: 0ffdadea0b92
Create Date: 2017-09-01 15:59:56.936727

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b14e7aca2366"
down_revision = "0ffdadea0b92"
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
    op.add_column("physical_measurements", sa.Column("created_site_id", sa.Integer(), nullable=True))
    op.add_column("physical_measurements", sa.Column("created_username", sa.String(length=255), nullable=True))
    op.add_column("physical_measurements", sa.Column("finalized_site_id", sa.Integer(), nullable=True))
    op.add_column("physical_measurements", sa.Column("finalized_username", sa.String(length=255), nullable=True))
    op.create_foreign_key(None, "physical_measurements", "site", ["finalized_site_id"], ["site_id"])
    op.create_foreign_key(None, "physical_measurements", "site", ["created_site_id"], ["site_id"])
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "physical_measurements", type_="foreignkey")
    op.drop_constraint(None, "physical_measurements", type_="foreignkey")
    op.drop_column("physical_measurements", "finalized_username")
    op.drop_column("physical_measurements", "finalized_site_id")
    op.drop_column("physical_measurements", "created_username")
    op.drop_column("physical_measurements", "created_site_id")
    # ### end Alembic commands ###
