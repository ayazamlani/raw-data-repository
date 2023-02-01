"""genomic_set_member history table

Revision ID: e8f8bcc55286
Revises: f69e4a978a1f, 78ab5fe99ad1
Create Date: 2022-03-22 13:31:20.292435

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import rdr_service.model.utils


from rdr_service.participant_enums import PhysicalMeasurementsStatus, QuestionnaireStatus, OrderStatus
from rdr_service.participant_enums import WithdrawalStatus, WithdrawalReason, SuspensionStatus, QuestionnaireDefinitionStatus
from rdr_service.participant_enums import EnrollmentStatus, Race, SampleStatus, OrganizationType, BiobankOrderStatus
from rdr_service.participant_enums import OrderShipmentTrackingStatus, OrderShipmentStatus
from rdr_service.participant_enums import MetricSetType, MetricsKey, GenderIdentity
from rdr_service.model.base import add_table_history_table, drop_table_history_table
from rdr_service.model.code import CodeType
from rdr_service.model.site_enums import SiteStatus, EnrollingStatus, DigitalSchedulingStatus, ObsoleteStatus

# revision identifiers, used by Alembic.
revision = '57515daf8448'
down_revision = '2bda73fa67b2'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('genomic_set_member', 'genomic_workflow_state_history')
    op.execute("""
        CREATE TABLE genomic_set_member_history LIKE genomic_set_member;

        ALTER TABLE genomic_set_member_history
        CHANGE COLUMN `id` `id` INTEGER NOT NULL,
        DROP PRIMARY KEY,
        ADD revision_action VARCHAR(8) DEFAULT 'insert' FIRST,
        ADD revision_id INT(6) NOT NULL AFTER revision_action,
        ADD revision_dt DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) AFTER revision_id;

        ALTER TABLE genomic_set_member_history
        ADD INDEX idx_revision (revision_id),
        CHANGE COLUMN `revision_id` `revision_id` INT(6) NOT NULL AUTO_INCREMENT,
        ADD PRIMARY KEY (`id`, revision_id);

        ALTER TABLE genomic_set_member_history
            DROP COLUMN modified,
            DROP COLUMN reconcile_metrics_bb_manifest_job_run_id,
            DROP COLUMN reconcile_gc_manifest_job_run_id,
            DROP COLUMN reconcile_metrics_sequencing_job_run_id,
            DROP COLUMN reconcile_cvl_job_run_id,
            DROP COLUMN gem_a1_manifest_job_run_id,
            DROP COLUMN gem_a2_manifest_job_run_id,
            DROP COLUMN gem_a3_manifest_job_run_id,
            DROP COLUMN aw3_manifest_job_run_id,
            DROP COLUMN aw4_manifest_job_run_id,
            DROP COLUMN aw2f_manifest_job_run_id,
            DROP COLUMN cvl_w1_manifest_job_run_id,
            DROP COLUMN cvl_w2_manifest_job_run_id,
            DROP COLUMN cvl_w3_manifest_job_run_id,
            DROP COLUMN cvl_w4_manifest_job_run_id,
            DROP COLUMN cvl_w4f_manifest_job_run_id,
            DROP COLUMN cvl_aw1c_manifest_job_run_id,
            DROP COLUMN cvl_aw1cf_manifest_job_run_id,
            DROP COLUMN cvl_w3sr_manifest_job_run_id,
            DROP COLUMN cvl_w2sc_manifest_job_run_id,
            DROP COLUMN color_metrics_job_run_id,
            DROP COLUMN cvl_w1il_pgx_job_run_id,
            DROP COLUMN cvl_w1il_hdr_job_run_id,
            DROP COLUMN cvl_w4wr_pgx_manifest_job_run_id,
            DROP COLUMN cvl_w4wr_hdr_manifest_job_run_id,
            DROP COLUMN cvl_w3sc_manifest_job_run_id,
            DROP COLUMN cvl_w3ns_manifest_job_run_id;
    """)
    op.execute("""
        CREATE TRIGGER genomic_set_member__ai AFTER INSERT ON genomic_set_member FOR EACH ROW
                INSERT INTO genomic_set_member_history (revision_action, revision_dt, id, created, genomic_set_id, participant_id, ny_flag, sex_at_birth, genome_type, ai_an, biobank_id, package_id, validation_status, validation_flags, validated_time, collection_tube_id, sample_id, sample_type, sequencing_file_name, gc_site_id, gc_manifest_box_storage_unit_id, gc_manifest_box_plate_id, gc_manifest_well_position, gc_manifest_parent_sample_id, gc_manifest_matrix_id, gc_manifest_treatments, gc_manifest_quantity_ul, gc_manifest_total_concentration_ng_per_ul, gc_manifest_total_dna_ng, gc_manifest_visit_description, gc_manifest_sample_source, gc_manifest_study, gc_manifest_tracking_number, gc_manifest_contact, gc_manifest_email, gc_manifest_study_pi, gc_manifest_test_name, gc_manifest_failure_mode, gc_manifest_failure_description, aw1_file_processed_id, aw2_file_processed_id, gem_pass, gem_date_of_import, aw3_manifest_file_id, aw0_manifest_file_id, gem_metrics_ancestry_loop_response, gem_metrics_available_results, gem_metrics_results_released_at, genomic_workflow_state, genomic_workflow_state_str, genomic_workflow_state_modified_time, report_consent_removal_date, qc_status, qc_status_str, fingerprint_path, dev_note, replated_member_id, ignore_flag, block_research, block_research_reason, block_results, block_results_reason, participant_origin, cvl_secondary_conf_failure)
                SELECT 'insert', NOW(6), id, created, genomic_set_id, participant_id, ny_flag, sex_at_birth, genome_type, ai_an, biobank_id, package_id, validation_status, validation_flags, validated_time, collection_tube_id, sample_id, sample_type, sequencing_file_name, gc_site_id, gc_manifest_box_storage_unit_id, gc_manifest_box_plate_id, gc_manifest_well_position, gc_manifest_parent_sample_id, gc_manifest_matrix_id, gc_manifest_treatments, gc_manifest_quantity_ul, gc_manifest_total_concentration_ng_per_ul, gc_manifest_total_dna_ng, gc_manifest_visit_description, gc_manifest_sample_source, gc_manifest_study, gc_manifest_tracking_number, gc_manifest_contact, gc_manifest_email, gc_manifest_study_pi, gc_manifest_test_name, gc_manifest_failure_mode, gc_manifest_failure_description, aw1_file_processed_id, aw2_file_processed_id, gem_pass, gem_date_of_import, aw3_manifest_file_id, aw0_manifest_file_id, gem_metrics_ancestry_loop_response, gem_metrics_available_results, gem_metrics_results_released_at, genomic_workflow_state, genomic_workflow_state_str, genomic_workflow_state_modified_time, report_consent_removal_date, qc_status, qc_status_str, fingerprint_path, dev_note, replated_member_id, ignore_flag, block_research, block_research_reason, block_results, block_results_reason, participant_origin, cvl_secondary_conf_failure
                FROM genomic_set_member AS d WHERE d.id = NEW.id;

            CREATE TRIGGER genomic_set_member__au AFTER UPDATE ON genomic_set_member FOR EACH ROW
                INSERT INTO genomic_set_member_history (revision_action, revision_dt, id, created, genomic_set_id, participant_id, ny_flag, sex_at_birth, genome_type, ai_an, biobank_id, package_id, validation_status, validation_flags, validated_time, collection_tube_id, sample_id, sample_type, sequencing_file_name, gc_site_id, gc_manifest_box_storage_unit_id, gc_manifest_box_plate_id, gc_manifest_well_position, gc_manifest_parent_sample_id, gc_manifest_matrix_id, gc_manifest_treatments, gc_manifest_quantity_ul, gc_manifest_total_concentration_ng_per_ul, gc_manifest_total_dna_ng, gc_manifest_visit_description, gc_manifest_sample_source, gc_manifest_study, gc_manifest_tracking_number, gc_manifest_contact, gc_manifest_email, gc_manifest_study_pi, gc_manifest_test_name, gc_manifest_failure_mode, gc_manifest_failure_description, aw1_file_processed_id, aw2_file_processed_id, gem_pass, gem_date_of_import, aw3_manifest_file_id, aw0_manifest_file_id, gem_metrics_ancestry_loop_response, gem_metrics_available_results, gem_metrics_results_released_at, genomic_workflow_state, genomic_workflow_state_str, genomic_workflow_state_modified_time, report_consent_removal_date, qc_status, qc_status_str, fingerprint_path, dev_note, replated_member_id, ignore_flag, block_research, block_research_reason, block_results, block_results_reason, participant_origin, cvl_secondary_conf_failure)
                SELECT 'update', NOW(6), id, created, genomic_set_id, participant_id, ny_flag, sex_at_birth, genome_type, ai_an, biobank_id, package_id, validation_status, validation_flags, validated_time, collection_tube_id, sample_id, sample_type, sequencing_file_name, gc_site_id, gc_manifest_box_storage_unit_id, gc_manifest_box_plate_id, gc_manifest_well_position, gc_manifest_parent_sample_id, gc_manifest_matrix_id, gc_manifest_treatments, gc_manifest_quantity_ul, gc_manifest_total_concentration_ng_per_ul, gc_manifest_total_dna_ng, gc_manifest_visit_description, gc_manifest_sample_source, gc_manifest_study, gc_manifest_tracking_number, gc_manifest_contact, gc_manifest_email, gc_manifest_study_pi, gc_manifest_test_name, gc_manifest_failure_mode, gc_manifest_failure_description, aw1_file_processed_id, aw2_file_processed_id, gem_pass, gem_date_of_import, aw3_manifest_file_id, aw0_manifest_file_id, gem_metrics_ancestry_loop_response, gem_metrics_available_results, gem_metrics_results_released_at, genomic_workflow_state, genomic_workflow_state_str, genomic_workflow_state_modified_time, report_consent_removal_date, qc_status, qc_status_str, fingerprint_path, dev_note, replated_member_id, ignore_flag, block_research, block_research_reason, block_results, block_results_reason, participant_origin, cvl_secondary_conf_failure
                FROM genomic_set_member AS d
                WHERE d.id = NEW.id
                    AND (
                        NEW.id <=> OLD.id OR
                        NEW.created <=> OLD.created OR
                        NEW.genomic_set_id <=> OLD.genomic_set_id OR
                        NEW.participant_id <=> OLD.participant_id OR
                        NEW.ny_flag <=> OLD.ny_flag OR
                        NEW.sex_at_birth <=> OLD.sex_at_birth OR
                        NEW.genome_type <=> OLD.genome_type OR
                        NEW.ai_an <=> OLD.ai_an OR
                        NEW.biobank_id <=> OLD.biobank_id OR
                        NEW.package_id <=> OLD.package_id OR
                        NEW.validation_status <=> OLD.validation_status OR
                        NEW.validation_flags <=> OLD.validation_flags OR
                        NEW.validated_time <=> OLD.validated_time OR
                        NEW.collection_tube_id <=> OLD.collection_tube_id OR
                        NEW.sample_id <=> OLD.sample_id OR
                        NEW.sample_type <=> OLD.sample_type OR
                        NEW.sequencing_file_name <=> OLD.sequencing_file_name OR
                        NEW.gc_site_id <=> OLD.gc_site_id OR
                        NEW.gc_manifest_box_storage_unit_id <=> OLD.gc_manifest_box_storage_unit_id OR
                        NEW.gc_manifest_box_plate_id <=> OLD.gc_manifest_box_plate_id OR
                        NEW.gc_manifest_well_position <=> OLD.gc_manifest_well_position OR
                        NEW.gc_manifest_parent_sample_id <=> OLD.gc_manifest_parent_sample_id OR
                        NEW.gc_manifest_matrix_id <=> OLD.gc_manifest_matrix_id OR
                        NEW.gc_manifest_treatments <=> OLD.gc_manifest_treatments OR
                        NEW.gc_manifest_quantity_ul <=> OLD.gc_manifest_quantity_ul OR
                        NEW.gc_manifest_total_concentration_ng_per_ul <=> OLD.gc_manifest_total_concentration_ng_per_ul OR
                        NEW.gc_manifest_total_dna_ng <=> OLD.gc_manifest_total_dna_ng OR
                        NEW.gc_manifest_visit_description <=> OLD.gc_manifest_visit_description OR
                        NEW.gc_manifest_sample_source <=> OLD.gc_manifest_sample_source OR
                        NEW.gc_manifest_study <=> OLD.gc_manifest_study OR
                        NEW.gc_manifest_tracking_number <=> OLD.gc_manifest_tracking_number OR
                        NEW.gc_manifest_contact <=> OLD.gc_manifest_contact OR
                        NEW.gc_manifest_email <=> OLD.gc_manifest_email OR
                        NEW.gc_manifest_study_pi <=> OLD.gc_manifest_study_pi OR
                        NEW.gc_manifest_test_name <=> OLD.gc_manifest_test_name OR
                        NEW.gc_manifest_failure_mode <=> OLD.gc_manifest_failure_mode OR
                        NEW.gc_manifest_failure_description <=> OLD.gc_manifest_failure_description OR
                        NEW.aw1_file_processed_id <=> OLD.aw1_file_processed_id OR
                        NEW.aw2_file_processed_id <=> OLD.aw2_file_processed_id OR
                        NEW.gem_pass <=> OLD.gem_pass OR
                        NEW.gem_date_of_import <=> OLD.gem_date_of_import OR
                        NEW.aw3_manifest_file_id <=> OLD.aw3_manifest_file_id OR
                        NEW.aw0_manifest_file_id <=> OLD.aw0_manifest_file_id OR
                        NEW.gem_metrics_ancestry_loop_response <=> OLD.gem_metrics_ancestry_loop_response OR
                        NEW.gem_metrics_available_results <=> OLD.gem_metrics_available_results OR
                        NEW.gem_metrics_results_released_at <=> OLD.gem_metrics_results_released_at OR
                        NEW.genomic_workflow_state <=> OLD.genomic_workflow_state OR
                        NEW.genomic_workflow_state_str <=> OLD.genomic_workflow_state_str OR
                        NEW.genomic_workflow_state_modified_time <=> OLD.genomic_workflow_state_modified_time OR
                        NEW.report_consent_removal_date <=> OLD.report_consent_removal_date OR
                        NEW.qc_status <=> OLD.qc_status OR
                        NEW.qc_status_str <=> OLD.qc_status_str OR
                        NEW.fingerprint_path <=> OLD.fingerprint_path OR
                        NEW.dev_note <=> OLD.dev_note OR
                        NEW.replated_member_id <=> OLD.replated_member_id OR
                        NEW.ignore_flag <=> OLD.ignore_flag OR
                        NEW.block_research <=> OLD.block_research OR
                        NEW.block_research_reason <=> OLD.block_research_reason OR
                        NEW.block_results <=> OLD.block_results OR
                        NEW.block_results_reason <=> OLD.block_results_reason OR
                        NEW.participant_origin <=> OLD.participant_origin OR
                        NEW.cvl_secondary_conf_failure <=> OLD.cvl_secondary_conf_failure
                    );

        CREATE TRIGGER genomic_set_member__bd BEFORE DELETE ON genomic_set_member FOR EACH ROW
            INSERT INTO genomic_set_member_history (revision_action, revision_dt, id, created, genomic_set_id, participant_id, ny_flag, sex_at_birth, genome_type, ai_an, biobank_id, package_id, validation_status, validation_flags, validated_time, collection_tube_id, sample_id, sample_type, sequencing_file_name, gc_site_id, gc_manifest_box_storage_unit_id, gc_manifest_box_plate_id, gc_manifest_well_position, gc_manifest_parent_sample_id, gc_manifest_matrix_id, gc_manifest_treatments, gc_manifest_quantity_ul, gc_manifest_total_concentration_ng_per_ul, gc_manifest_total_dna_ng, gc_manifest_visit_description, gc_manifest_sample_source, gc_manifest_study, gc_manifest_tracking_number, gc_manifest_contact, gc_manifest_email, gc_manifest_study_pi, gc_manifest_test_name, gc_manifest_failure_mode, gc_manifest_failure_description, aw1_file_processed_id, aw2_file_processed_id, gem_pass, gem_date_of_import, aw3_manifest_file_id, aw0_manifest_file_id, gem_metrics_ancestry_loop_response, gem_metrics_available_results, gem_metrics_results_released_at, genomic_workflow_state, genomic_workflow_state_str, genomic_workflow_state_modified_time, report_consent_removal_date, qc_status, qc_status_str, fingerprint_path, dev_note, replated_member_id, ignore_flag, block_research, block_research_reason, block_results, block_results_reason, participant_origin, cvl_secondary_conf_failure)
            SELECT 'delete', NOW(6), id, created, genomic_set_id, participant_id, ny_flag, sex_at_birth, genome_type, ai_an, biobank_id, package_id, validation_status, validation_flags, validated_time, collection_tube_id, sample_id, sample_type, sequencing_file_name, gc_site_id, gc_manifest_box_storage_unit_id, gc_manifest_box_plate_id, gc_manifest_well_position, gc_manifest_parent_sample_id, gc_manifest_matrix_id, gc_manifest_treatments, gc_manifest_quantity_ul, gc_manifest_total_concentration_ng_per_ul, gc_manifest_total_dna_ng, gc_manifest_visit_description, gc_manifest_sample_source, gc_manifest_study, gc_manifest_tracking_number, gc_manifest_contact, gc_manifest_email, gc_manifest_study_pi, gc_manifest_test_name, gc_manifest_failure_mode, gc_manifest_failure_description, aw1_file_processed_id, aw2_file_processed_id, gem_pass, gem_date_of_import, aw3_manifest_file_id, aw0_manifest_file_id, gem_metrics_ancestry_loop_response, gem_metrics_available_results, gem_metrics_results_released_at, genomic_workflow_state, genomic_workflow_state_str, genomic_workflow_state_modified_time, report_consent_removal_date, qc_status, qc_status_str, fingerprint_path, dev_note, replated_member_id, ignore_flag, block_research, block_research_reason, block_results, block_results_reason, participant_origin, cvl_secondary_conf_failure
            FROM genomic_set_member AS d WHERE d.id = OLD.id;
    """)
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
            DROP TRIGGER IF EXISTS genomic_set_member__ai;
            DROP TRIGGER IF EXISTS genomic_set_member__au;
            DROP TRIGGER IF EXISTS genomic_set_member__bd;
        """)
    op.drop_table('genomic_set_member_history')
    op.add_column('genomic_set_member',
                  sa.Column('genomic_workflow_state_history', mysql.JSON(), nullable=True))

    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
