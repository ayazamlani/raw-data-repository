"""Add ID verification fields to participant_summary

Revision ID: a3711bb1ef9d
Revises: f3949fe06833, a3e5d5f020c1, 84fbc68c9bdd
Create Date: 2022-08-04 11:16:58.356637

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils


from rdr_service.participant_enums import OnSiteVerificationType, OnSiteVerificationVisitType

# revision identifiers, used by Alembic.
revision = 'a3711bb1ef9d'
down_revision = ('f3949fe06833', 'a3e5d5f020c1', '84fbc68c9bdd')
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
    op.add_column('participant_summary', sa.Column('onsite_id_verification_type', rdr_service.model.utils.Enum(OnSiteVerificationType), nullable=True))
    op.add_column('participant_summary', sa.Column('onsite_id_verification_visit_type', rdr_service.model.utils.Enum(OnSiteVerificationVisitType), nullable=True))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participant_summary', 'onsite_id_verification_visit_type')
    op.drop_column('participant_summary', 'onsite_id_verification_type')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
