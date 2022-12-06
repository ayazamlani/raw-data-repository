"""cdr_etl_history

Revision ID: 4d2ce3440f21
Revises: 136e4ea3caa2, a76200c8b07a
Create Date: 2022-05-16 14:30:04.101288

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils


from rdr_service.participant_enums import CdrEtlCodeType, CdrEtlSurveyStatus

# revision identifiers, used by Alembic.
revision = '4d2ce3440f21'
down_revision = ('136e4ea3caa2', 'a76200c8b07a')
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
    op.create_table('cdr_etl_run_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=True),
    sa.Column('modified', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=True),
    sa.Column('start_time', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=False),
    sa.Column('end_time', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=True),
    sa.Column('vocabulary_path', sa.String(length=256), nullable=True),
    sa.Column('cut_off_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cdr_etl_survey_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=True),
    sa.Column('modified', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=True),
    sa.Column('etl_run_id', sa.Integer(), nullable=False),
    sa.Column('code_id', sa.Integer(), nullable=True),
    sa.Column('code_value', sa.String(length=80), nullable=True),
    sa.Column('code_type', rdr_service.model.utils.Enum(CdrEtlCodeType), nullable=True),
    sa.Column('status', rdr_service.model.utils.Enum(CdrEtlSurveyStatus), nullable=True),
    sa.ForeignKeyConstraint(['code_id'], ['code.code_id'], ),
    sa.ForeignKeyConstraint(['etl_run_id'], ['cdr_etl_run_history.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cdr_excluded_code',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=True),
    sa.Column('modified', rdr_service.model.utils.UTCDateTime6(fsp=6), nullable=True),
    sa.Column('code_id', sa.Integer(), nullable=True),
    sa.Column('code_value', sa.String(length=80), nullable=True),
    sa.Column('code_type', rdr_service.model.utils.Enum(CdrEtlCodeType), nullable=True),
    sa.ForeignKeyConstraint(['code_id'], ['code.code_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cdr_excluded_code')
    op.drop_table('cdr_etl_survey_history')
    op.drop_table('cdr_etl_run_history')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
