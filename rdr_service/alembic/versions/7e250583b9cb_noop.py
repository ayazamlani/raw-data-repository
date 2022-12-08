"""add_qra_qr_id

Revision ID: 7e250583b9cb
Revises: 89dd3b8f4447
Create Date: 2017-10-05 15:06:41.213664

"""

# revision identifiers, used by Alembic.
revision = "7e250583b9cb"
down_revision = "89dd3b8f4447"
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
    # View is replaced entirely in later migration.
    pass


def downgrade_rdr():
    pass
