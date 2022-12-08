"""Deidentify ppi views

Revision ID: 04564bf1b5e8
Revises: 6f9266e7a5fb
Create Date: 2017-12-20 13:21:37.487290

"""

# revision identifiers, used by Alembic.
revision = "04564bf1b5e8"
down_revision = "6f9266e7a5fb"
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()


def upgrade_rdr():
    pass


def downgrade_rdr():
    pass


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
