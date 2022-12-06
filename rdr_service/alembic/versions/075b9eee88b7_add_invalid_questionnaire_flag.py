"""add invalid questionnaire flag

Revision ID: 075b9eee88b7
Revises: 9f0935df44bb
Create Date: 2018-07-18 13:07:58.598473

"""
import model.utils
import sqlalchemy as sa
from alembic import op

from rdr_service.participant_enums import QuestionnaireDefinitionStatus

# revision identifiers, used by Alembic.
revision = "075b9eee88b7"
down_revision = "9f0935df44bb"
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
    op.add_column("questionnaire", sa.Column("status", model.utils.Enum(QuestionnaireDefinitionStatus), nullable=True))
    op.add_column(
        "questionnaire_history", sa.Column("status", model.utils.Enum(QuestionnaireDefinitionStatus), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("questionnaire_history", "status")
    op.drop_column("questionnaire", "status")
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
