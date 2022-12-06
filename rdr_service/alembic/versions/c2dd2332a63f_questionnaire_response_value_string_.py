"""Questionnaire response value_string from varchar to text

Revision ID: c2dd2332a63f
Revises: 32d414bc9a1e
Create Date: 2018-02-09 15:27:44.921089

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c2dd2332a63f"
down_revision = "32d414bc9a1e"
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
    op.alter_column(
        "questionnaire_response_answer",
        "value_string",
        existing_type=sa.String(1024),
        type_=sa.Text(),
        existing_nullable=True,
    )


def downgrade_rdr():
    op.alter_column(
        "questionnaire_response_answer",
        "value_string",
        existing_type=sa.Text(),
        type_=sa.String(1024),
        existing_nullable=True,
    )


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
