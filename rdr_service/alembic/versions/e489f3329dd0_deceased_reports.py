"""deceased reports

Revision ID: e489f3329dd0
Revises: a51ea1c0bfbf
Create Date: 2020-08-04 16:07:35.869151

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils


from rdr_service.participant_enums import DeceasedNotification, DeceasedReportDenialReason, DeceasedReportStatus

# revision identifiers, used by Alembic.
revision = 'e489f3329dd0'
down_revision = 'a51ea1c0bfbf'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('system', sa.String(length=80), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('api_username_system', 'api_user', ['system', 'username'], unique=False)
    op.create_table('deceased_report',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', rdr_service.model.utils.UTCDateTime(), nullable=False),
    sa.Column('last_modified', rdr_service.model.utils.UTCDateTime(), nullable=False),
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('date_of_death', sa.Date(), nullable=True),
    sa.Column('notification', rdr_service.model.utils.Enum(DeceasedNotification), nullable=False),
    sa.Column('notification_other', sa.String(length=1024), nullable=True),
    sa.Column('reporter_name', sa.String(length=255), nullable=True),
    sa.Column('reporter_relationship', sa.String(length=8), nullable=True),
    sa.Column('reporter_email', sa.String(length=255), nullable=True),
    sa.Column('reporter_phone', sa.String(length=16), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('authored', rdr_service.model.utils.UTCDateTime(), nullable=False),
    sa.Column('reviewer_id', sa.Integer(), nullable=True),
    sa.Column('reviewed', rdr_service.model.utils.UTCDateTime(), nullable=True),
    sa.Column('status', rdr_service.model.utils.Enum(DeceasedReportStatus), nullable=False),
    sa.Column('denial_reason', rdr_service.model.utils.Enum(DeceasedReportDenialReason), nullable=True),
    sa.Column('denial_reason_other', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['api_user.id'], ),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.participant_id'], ),
    sa.ForeignKeyConstraint(['reviewer_id'], ['api_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deceased_report')
    op.drop_index('api_username_system', table_name='api_user')
    op.drop_table('api_user')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
