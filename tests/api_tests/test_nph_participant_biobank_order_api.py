# Sample ID = NP124820391
from datetime import datetime
import json
from sqlalchemy.orm import Query
from unittest.mock import MagicMock, patch

from tests.helpers.unittest_base import BaseTestCase
from rdr_service.dao import database_factory
from rdr_service.main import app
from rdr_service.model.study_nph import (
    StudyCategory, Order, OrderedSample, Participant, SampleUpdate, Site
)


BLOOD_SAMPLE = {
    "subject": "Patient/P124820391",
    "identifier": [{
        "system": "http://www.pmi-ops.org/order-id",
        "value": "nph-order-id-123"
    }, {
        "system": "http://www.pmi-ops.org/sample-id",
        "value": "nph-sample-id-456"
    },  {
            "system": "https://www.pmi-ops.org/client-id",
            "value": "7042688"
    }],
    "createdInfo": {
        "author": {
            "system": "https://www.pmi-ops.org\/nph-username",
            "value": "test@example.com"
        },
        "site": {
            "system": "https://www.pmi-ops.org\/site-id",
            "value": "nph-site-testa"
        }
    },
    "collectedInfo": {
        "author": {
            "system": "https://www.pmi-ops.org\/nph-username",
            "value": "test@example.com"
        },
        "site": {
            "system": "https://www.pmi-ops.org\/site-id",
            "value": "nph-site-testa"
        }
    },
    "finalizedInfo": {
        "author": {
            "system": "https://www.pmi-ops.org\/nph-username",
            "value": "test@example.com"
        },
        "site": {
            "system": "https://www.pmi-ops.org\/site-id",
            "value": "hpo-site-testa"
        }
    },
    "created": "2022-11-03T09:40:21Z",
    "module": "1",
    "visitType": "LMT",
    "timepoint": "15min",
    "sample": {
        "test": "PST8",
        "description": "8 mL PST",
        "collected": "2022-11-03T09:45:49Z",
        "finalized": "2022-11-03T10:55:41Z"
    },
    "aliquots": [{
        "id": "123",
        "identifier": "LHPSTP1",
        "container": "1.4mL Matrix Tube (500 uL)",
        "volume": "450",
        "units": "uL",
        "description": "1.4 mL matrix tubes",
        "collected": "2022-11-03T09:45:49Z"
    }, {
        "id": "456",
        "identifier": "LHPSTP1",
        "container": "1.4mL Matrix Tube (1000 uL)",
        "volume": "970",
        "units": "uL",
        "description": "1.4 mL matrix tubes",
        "collected": "2022-11-03T09:45:49Z"
    }, {
        "id": "789",
        "identifier": "LHPSTP1",
        "container": "1.4mL Matrix Tube (1000 uL)",
        "volume": "970",
        "units": "uL",
        "description": "1.4 mL matrix tubes",
        "collected": "2022-11-03T09:45:49Z"
    }, ],
    "notes": {
        "collected": "Test notes 1",
        "finalized": "Test notes 2"
    }
}

PATCH_SAMPLE = {
                "status": "restored",
                "amendedReason": "ORDER_RESTORE_WRONG_PARTICIPANT",
                "restoredInfo": {
                      "author": {
                                    "system": "https://www.pmi-ops.org/nph-username",
                                    "value": "test@pmi-ops.org"
                      },
                      "site": {
                                "system": "https://www.pmi-ops.org/site-id",
                                "value": "nph-site-testa"
                       }
                }
}

PATCH_CANCEL_SAMPLE = {
                "status": "cancelled",
                "amendedReason": "CANCEL_ERROR",
                "cancelledInfo": {
                      "author": {
                                    "system": "https://www.pmi-ops.org/nph-username",
                                    "value": "test@pmi-ops.org"
                      },
                      "site": {
                                "system": "https://www.pmi-ops.org/site-id",
                                "value": "nph-site-testa"
                       }
                }
}


class TestNPHParticipantOrderAPI(BaseTestCase):

    @patch('rdr_service.dao.study_nph_dao.Query.filter')
    @patch('rdr_service.api.nph_participant_biobank_order_api.database_factory')
    @patch('rdr_service.dao.study_nph_dao.NphParticipantDao.get_participant')
    @patch('rdr_service.dao.study_nph_dao.NphSiteDao.get_id')
    def test_post(self, site_id, pid, database_factor, query_filter):
        query_filter.return_value.first.return_value = StudyCategory()
        database_factor.return_value.session.return_value = MagicMock()
        pid.return_value = Participant(id=124820391)
        site_id.return_value = 1
        queries = [BLOOD_SAMPLE]
        for query in queries:
            executed = app.test_client().post('rdr/v1/api/v1/nph/Participant/1000124820391/BiobankOrder', json=query)
            result = json.loads(executed.data.decode('utf-8'))
            for k, _ in result.items():
                if k.upper() != "ID":
                    self.assertEqual(query.get(k), result.get(k))
        with database_factory.get_database().session() as session:
            query = Query(SampleUpdate)
            query.session = session
            sample_update_result = query.all()
            for each in sample_update_result:
                self.assertIsNotNone(each.ordered_sample_json)

    @patch('rdr_service.dao.study_nph_dao.NphOrderDao.get_order')
    @patch('rdr_service.api.nph_participant_biobank_order_api.database_factory')
    @patch('rdr_service.dao.study_nph_dao.Query.filter')
    @patch('rdr_service.dao.study_nph_dao.NphSiteDao.get_id')
    def test_patch_update(self, site_id, query_filter, database_factor, order_id):
        order_id.return_value = Order(id=1, participant_id=124820391)
        database_factor.return_value.session.return_value = MagicMock()
        query_filter.return_value.first.return_value = Participant(id=124820391)
        site_id.return_value = 1
        queries = [PATCH_SAMPLE]
        for query in queries:
            executed = app.test_client().patch('rdr/v1/api/v1/nph/Participant/1000124820391/BiobankOrder/1', json=query)
            result = json.loads(executed.data.decode('utf-8'))
            for k, _ in result.items():
                if k.upper() != "ID":
                    self.assertEqual(query.get(k), result.get(k))

    @patch('rdr_service.dao.study_nph_dao.NphSiteDao.get_id')
    def test_patch_cancel(self, site_id):
        participant = Participant(id=12345, biobank_id=12345)
        site = Site(id=1)
        self.session.add(participant)
        self.session.add(site)
        self.session.commit()
        self.session.add(
            Order(
                id=1,
                participant_id=participant.id,
                notes={},
                samples=[
                    OrderedSample(id=1, collected=datetime.utcnow()),
                    OrderedSample(id=2)
                ]
            )
        )
        self.session.commit()

        site_id.return_value = 1
        patch_json = PATCH_CANCEL_SAMPLE

        response = self.send_patch(f'api/v1/nph/Participant/1000{participant.id}/BiobankOrder/1', patch_json)

        del response['id']
        self.assertDictEqual(patch_json, response)

        sample_update_list = self.session.query(SampleUpdate).all()
        self.assertListEqual([1, 2], [sample_update.rdr_ordered_sample_id for sample_update in sample_update_list])

    @patch('rdr_service.dao.study_nph_dao.NphSiteDao.get_id')
    def test_patch_aliquot_update(self, site_id):
        participant = Participant(id=12345, biobank_id=12345)
        site = Site(id=1)
        self.session.add(participant)
        self.session.add(site)
        self.session.commit()
        test_order = Order(
            id=1,
            participant_id=participant.id,
            notes={},
            samples=[
                OrderedSample(
                    id=1,
                    description='update this',
                    children=[
                        OrderedSample(aliquot_id='a12', volume='error'),
                        OrderedSample(aliquot_id='c34', description='to be cancelled')
                    ]
                )
            ]
        )
        self.session.add(test_order)
        self.session.commit()

        site_id.return_value = 1

        self.send_patch(
            f'api/v1/nph/Participant/1000{participant.id}/BiobankOrder/1',
            {
                'status': 'amended',
                "amendedInfo": {
                    "author": {
                        "system": "https://www.pmi-ops.org\/nph-username",
                        "value": "test@example.com"
                    },
                    "site": {
                        "system": "https://www.pmi-ops.org\/site-id",
                        "value": "nph-site-testa"
                    }
                },
                'sample': {
                    'description': 'updated'
                },
                "aliquots": [
                    {
                        "id": "a12",
                        "volume": 450
                    }, {
                        "id": "456",
                        "identifier": "new1",
                        "container": "matrix tube",
                        "volume": "970",
                        "units": "uL",
                        "description": "1.4 mL matrix tubes",
                        "collected": "2022-11-03T09:45:49Z"
                    }
                ]
            }
        )

        self.session.expire_all()  # Force the order to be refresh
        db_order: Order = self.session.query(Order).filter(Order.id == 1).one()

        # check updates on parent sample
        parent_sample = db_order.samples[0]
        self.assertEqual('updated', parent_sample.description)

        for aliquot in parent_sample.children:
            if aliquot.aliquot_id == 'a12':  # check that the volume updated
                self.assertEqual('450', aliquot.volume)
            elif aliquot.aliquot_id == 'c34':  # check that the aliquot got cancelled
                self.assertEqual('cancelled', aliquot.status)

    @patch('rdr_service.dao.study_nph_dao.NphOrderedSampleDao._get_child_order_sample')
    @patch('rdr_service.dao.study_nph_dao.NphOrderedSampleDao._get_parent_order_sample')
    @patch('rdr_service.dao.study_nph_dao.NphStudyCategoryDao.get_study_category_sample')
    @patch('rdr_service.dao.study_nph_dao.NphOrderDao.check_order_exist')
    @patch('rdr_service.dao.study_nph_dao.NphOrderDao.get_order')
    @patch('rdr_service.api.nph_participant_biobank_order_api.database_factory')
    @patch('rdr_service.dao.study_nph_dao.NphParticipantDao.check_participant_exist')
    @patch('rdr_service.dao.study_nph_dao.Query.filter')
    @patch('rdr_service.dao.study_nph_dao.NphSiteDao.site_exist')
    @patch('rdr_service.dao.study_nph_dao.NphSiteDao.get_id')
    def test_put(self, site_id, site_exist, query_filter, p_exist, database_factor, order_id, order_exist,
                 sc_exist, parent_os, child_os):
        child_os.return_value = []
        parent_os.return_value = OrderedSample()
        sc_exist.return_value = StudyCategory(name="15min"), StudyCategory(name="LMT"), StudyCategory(name="1")
        p_exist.return_value = True
        order_exist.return_value = True, Order(id=1, participant_id=124820391)
        order_id.return_value = Order(id=1, participant_id=124820391)
        database_factor.return_value.session.return_value = MagicMock()
        query_filter.return_value.first.return_value = Participant(id=124820391)
        site_id.return_value = 1
        site_exist.return_value = True
        queries = [BLOOD_SAMPLE]
        for query in queries:
            executed = app.test_client().put('rdr/v1/api/v1/nph/Participant/1000124820391/BiobankOrder/1', json=query)
            result = json.loads(executed.data.decode('utf-8'))
            for k, _ in result.items():
                if k.upper() != "ID":
                    self.assertEqual(query.get(k), result.get(k))
        with database_factory.get_database().session() as session:
            query = Query(SampleUpdate)
            query.session = session
            result = query.all()
            for each in result:
                self.assertIsNotNone(each.ordered_sample_json)

    def tearDown(self):
        super().tearDown()
        self.clear_table_after_test("nph.ordered_sample")
        self.clear_table_after_test("nph.order")
        self.clear_table_after_test("nph.site")
        self.clear_table_after_test("nph.study_category")
        self.clear_table_after_test("nph.participant")
        self.clear_table_after_test("nph.sample_update")
