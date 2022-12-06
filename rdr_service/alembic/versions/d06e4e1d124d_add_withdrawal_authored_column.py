"""add withdrawal_authored column

Revision ID: d06e4e1d124d
Revises: 20e98a16ad20
Create Date: 2019-08-01 11:13:02.111028

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "d06e4e1d124d"
down_revision = "20e98a16ad20"
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
    op.execute("ALTER TABLE participant ADD COLUMN withdrawal_authored DATETIME(6) AFTER `withdrawal_time`;")
    op.execute("ALTER TABLE participant_history ADD COLUMN withdrawal_authored DATETIME(6) AFTER `withdrawal_time`;")
    op.execute("ALTER TABLE participant_summary ADD COLUMN withdrawal_authored DATETIME(6) AFTER `withdrawal_time`;")
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("participant_summary", "withdrawal_authored")
    op.drop_column("participant_history", "withdrawal_authored")
    op.drop_column("participant", "withdrawal_authored")
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
