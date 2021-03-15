"""
This module provides central location for all genomics_mappings
"""

genome_type_to_aw1_file_prefix = {
            "aou_array": "_GEN_",
            "aou_wgs": "_SEQ_",
        }

raw_aw1_to_genomic_set_member_fields = {
    "package_id": "packageId",
    "box_storageunit_id": "gcManifestBoxStorageUnitId",
    "box_id_plate_id": "gcManifestBoxPlateId",
    "well_position": "gcManifestWellPosition",
    "sample_id": "sampleId",
    "parent_sample_id": "gcManifestParentSampleId",
    "collection_tube_id": "collectionTubeId",
    "matrix_id": "gcManifestMatrixId",
    "sample_type": "sampleType",
    "treatments": "gcManifestTreatments",
    "quantity": "gcManifestQuantity_ul",
    "total_concentration": "gcManifestTotalConcentration_ng_per_ul",
    "total_dna": "gcManifestTotalDNA_ng",
    "visit_description": "gcManifestVisitDescription",
    "sample_source": "gcManifestSampleSource",
    "study": "gcManifestStudy",
    "tracking_number": "gcManifestTrackingNumber",
    "contact": "gcManifestContact",
    "email": "gcManifestEmail",
    "study_pi": "gcManifestStudyPI",
    "test_name": "gcManifestTestName",
    "failure_mode": "gcManifestFailureMode",
    "failure_mode_desc": "gcManifestFailureDescription"
}
