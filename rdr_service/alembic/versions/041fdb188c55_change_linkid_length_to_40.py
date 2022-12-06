"""change_linkId_length_to_40

Revision ID: 041fdb188c55
Revises: c7c4b2f17f46
Create Date: 2018-11-08 11:27:22.218256

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "041fdb188c55"
down_revision = "c7c4b2f17f46"
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
    op.alter_column(
        "questionnaire_question",
        "link_id",
        existing_type=mysql.VARCHAR(length=20),
        type_=sa.String(length=40),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "questionnaire_question",
        "link_id",
        existing_type=sa.String(length=40),
        type_=mysql.VARCHAR(length=20),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
