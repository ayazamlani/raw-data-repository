"""add self report info to pm

Revision ID: 1acebc691c3c
Revises: 4c288de779e7
Create Date: 2022-06-09 11:33:34.620769

"""
from alembic import op
import sqlalchemy as sa
import rdr_service.model.utils


from rdr_service.participant_enums import PhysicalMeasurementsCollectType, OriginMeasurementUnit


# revision identifiers, used by Alembic.
revision = '1acebc691c3c'
down_revision = '4c288de779e7'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant_summary', sa.Column('physical_measurements_collect_type',
                                                   rdr_service.model.utils.Enum(PhysicalMeasurementsCollectType),
                                                   nullable=True))
    op.add_column('physical_measurements', sa.Column('collect_type',
                                                     rdr_service.model.utils.Enum(PhysicalMeasurementsCollectType),
                                                     nullable=True))
    op.add_column('physical_measurements', sa.Column('origin', sa.String(length=255), nullable=True))
    op.add_column('physical_measurements', sa.Column('origin_measurement_unit',
                                                     rdr_service.model.utils.Enum(OriginMeasurementUnit),
                                                     nullable=True))
    op.add_column('physical_measurements', sa.Column('questionnaire_response_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'physical_measurements', 'questionnaire_response', ['questionnaire_response_id'],
                          ['questionnaire_response_id'])
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'physical_measurements', type_='foreignkey')
    op.drop_column('physical_measurements', 'questionnaire_response_id')
    op.drop_column('physical_measurements', 'origin_measurement_unit')
    op.drop_column('physical_measurements', 'origin')
    op.drop_column('physical_measurements', 'collect_type')
    op.drop_column('participant_summary', 'physical_measurements_collect_type')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

