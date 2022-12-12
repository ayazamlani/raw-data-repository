"""Calendar table

Revision ID: e4518d7d1af1
Revises: 3da004006210
Create Date: 2018-03-06 09:53:49.794389

"""
import datetime

from alembic import op
from sqlalchemy import Column, Date

# revision identifiers, used by Alembic.
revision = "e4518d7d1af1"
down_revision = "3da004006210"
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    calendar_table = op.create_table("calendar", Column("day", Date))
    curr_date = datetime.date(2017, 1, 1)
    date_dicts = []
    # Insert 500 years of dates
    for _ in range(0, 365 * 500):
        date_dicts.append({"day": curr_date})
        curr_date = curr_date + datetime.timedelta(days=1)
    op.bulk_insert(calendar_table, date_dicts)


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
