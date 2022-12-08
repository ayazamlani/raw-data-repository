"""update-ehr-metrics

Revision ID: 6057344ac521
Revises: e66de5f77cec
Create Date: 2019-03-13 16:08:08.895358

"""
import model.utils
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "6057344ac521"
down_revision = "e66de5f77cec"
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name):
    globals()[f"downgrade_{engine_name}"]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "hpo_counts_report",
        sa.Column("report_run_time", model.utils.UTCDateTime(), nullable=False),
        sa.Column("hpo_id", sa.Integer(), nullable=False),
        sa.Column("hpo_id_string", sa.String(length=20), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=True),
        sa.Column("person", sa.Integer(), nullable=True),
        sa.Column("person_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("condition_occurrence", sa.Integer(), nullable=True),
        sa.Column("condition_occurrence_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("procedure_occurrence", sa.Integer(), nullable=True),
        sa.Column("procedure_occurrence_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("drug_exposure", sa.Integer(), nullable=True),
        sa.Column("drug_exposure_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("visit_occurrence", sa.Integer(), nullable=True),
        sa.Column("visit_occurrence_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("measurement", sa.Integer(), nullable=True),
        sa.Column("measurement_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("observation", sa.Integer(), nullable=True),
        sa.Column("observation_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("device_exposure", sa.Integer(), nullable=True),
        sa.Column("device_exposure_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("death", sa.Integer(), nullable=True),
        sa.Column("death_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("provider", sa.Integer(), nullable=True),
        sa.Column("provider_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("specimen", sa.Integer(), nullable=True),
        sa.Column("specimen_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("location", sa.Integer(), nullable=True),
        sa.Column("location_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("care_site", sa.Integer(), nullable=True),
        sa.Column("care_site_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.Column("note", sa.Integer(), nullable=True),
        sa.Column("note_upload_time", model.utils.UTCDateTime(), nullable=True),
        sa.PrimaryKeyConstraint("report_run_time", "hpo_id"),
    )
    op.add_column("ehr_receipt", sa.Column("hpo_id", sa.Integer(), nullable=False))
    op.add_column("ehr_receipt", sa.Column("receipt_time", model.utils.UTCDateTime(), nullable=False))
    op.create_index(op.f("ix_ehr_receipt_receipt_time"), "ehr_receipt", ["receipt_time"], unique=False)
    op.drop_index("ix_ehr_receipt_recorded_time", table_name="ehr_receipt")
    op.drop_constraint("ehr_receipt_ibfk_2", "ehr_receipt", type_="foreignkey")
    op.drop_constraint("ehr_receipt_ibfk_1", "ehr_receipt", type_="foreignkey")
    op.create_foreign_key(None, "ehr_receipt", "hpo", ["hpo_id"], ["hpo_id"], ondelete="CASCADE")
    op.drop_column("ehr_receipt", "received_time")
    op.drop_column("ehr_receipt", "site_id")
    op.drop_column("ehr_receipt", "recorded_time")
    op.drop_column("ehr_receipt", "participant_id")
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "ehr_receipt",
        sa.Column("participant_id", mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    )
    op.add_column("ehr_receipt", sa.Column("recorded_time", mysql.DATETIME(), nullable=False))
    op.add_column(
        "ehr_receipt", sa.Column("site_id", mysql.INTEGER(display_width=11), autoincrement=False, nullable=False)
    )
    op.add_column("ehr_receipt", sa.Column("received_time", mysql.DATETIME(), nullable=False))
    op.drop_constraint(None, "ehr_receipt", type_="foreignkey")
    op.create_foreign_key(
        "ehr_receipt_ibfk_1", "ehr_receipt", "participant", ["participant_id"], ["participant_id"], ondelete="CASCADE"
    )
    op.create_foreign_key("ehr_receipt_ibfk_2", "ehr_receipt", "site", ["site_id"], ["site_id"], ondelete="CASCADE")
    op.create_index("ix_ehr_receipt_recorded_time", "ehr_receipt", ["recorded_time"], unique=False)
    op.drop_index(op.f("ix_ehr_receipt_receipt_time"), table_name="ehr_receipt")
    op.drop_column("ehr_receipt", "receipt_time")
    op.drop_column("ehr_receipt", "hpo_id")
    op.drop_table("hpo_counts_report")
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
