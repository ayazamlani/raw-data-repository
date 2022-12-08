"""Adding pm view

Revision ID: b315fec9aa4e
Revises: 9a5c2ef1038f
Create Date: 2017-11-10 10:07:29.266546

"""

# revision identifiers, used by Alembic.
revision = "b315fec9aa4e"
down_revision = "9a5c2ef1038f"
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
    # Views are replaced entirely in later migration.
    pass


def downgrade_rdr():
    pass
