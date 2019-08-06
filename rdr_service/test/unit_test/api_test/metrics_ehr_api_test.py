import datetime
import urllib

from rdr_service.clock import FakeClock
from rdr_service.dao.calendar_dao import CalendarDao
from rdr_service.dao.ehr_dao import EhrReceiptDao
from rdr_service.dao.hpo_dao import HPODao
from rdr_service.dao.organization_dao import OrganizationDao
from rdr_service.dao.participant_dao import ParticipantDao
from rdr_service.dao.participant_summary_dao import ParticipantSummaryDao
from rdr_service.dao.site_dao import SiteDao
from rdr_service.model.calendar import Calendar
from rdr_service.model.ehr import EhrReceipt
from rdr_service.model.hpo import HPO
from rdr_service.model.organization import Organization
from rdr_service.model.participant import Participant
from rdr_service.model.participant_summary import ParticipantSummary
from rdr_service.participant_enums import EnrollmentStatus, OrganizationType, QuestionnaireStatus, \
  TEST_HPO_ID, \
  TEST_HPO_NAME, WithdrawalStatus, make_primary_provider_link_for_name
from rdr_service.test.unit_test.unit_test_util import FlaskTestBase

REQUIRED_PPI_MODULE_COUNT = 3  # NOTE: could not import from config in test runner


def _questionnaire_response_url(participant_id):
  return 'Participant/%s/QuestionnaireResponse' % participant_id


def iter_dates(start, end):
  """
  generate datetime.date objects for each day from `start` to `end`
  """
  i = start
  while i <= end:
    yield i
    i += datetime.timedelta(days=1)


class MetricsEhrApiTestBase(FlaskTestBase):

  def setUp(self, **kwargs):
    super(MetricsEhrApiTestBase, self).setUp(use_mysql=True, **kwargs)
    self.dao = ParticipantDao()
    self.ps_dao = ParticipantSummaryDao()
    self.ehr_receipt_dao = EhrReceiptDao()
    self.ps = ParticipantSummary()
    self.calendar_dao = CalendarDao()
    self.site_dao = SiteDao()
    self.hpo_dao = HPODao()
    self.org_dao = OrganizationDao()

    self.hpo_test = self._make_hpo(hpoId=TEST_HPO_ID, name=TEST_HPO_NAME, displayName='Test',
                                   organizationType=OrganizationType.UNSET)

    self.hpo_foo = self._make_hpo(hpoId=10, name='FOO', displayName='Foo')
    self.hpo_bar = self._make_hpo(hpoId=11, name='BAR', displayName='Bar')

    self.org_foo_a = self._make_org(
      organizationId=10,
      externalId='FOO_A',
      displayName='Foo A',
      hpoId=self.hpo_foo.hpoId
    )
    self.org_bar_a = self._make_org(
      organizationId=11,
      externalId='BAR_A',
      displayName='Bar A',
      hpoId=self.hpo_bar.hpoId
    )

  def _make_hpo(self, **kwargs):
    hpo = HPO(**kwargs)
    self.hpo_dao.insert(hpo)
    return hpo

  def _make_org(self, **kwargs):
    org = Organization(**kwargs)
    self.org_dao.insert(org)
    return org

  def _make_participant(
    self, participant, first_name=None, last_name=None, hpo=None, organization=None,
    unconsented=False, time_int=None, time_study=None, time_mem=None, time_fp=None,
    time_fp_stored=None, gender_id=None, dob=None, state_id=None
  ):
    """
    Create a participant in a transient test database.

    Note: copied from ParticipantCountsOverTimeApiTest

    :param participant: Participant object
    :param first_name: First name
    :param last_name: Last name
    :param time_int: Time that participant fulfilled INTERESTED criteria
    :param time_mem: Time that participant fulfilled MEMBER criteria
    :param time_fp: Time that participant fulfilled FULL_PARTICIPANT criteria
    :return: Participant object
    """

    participant.hpoId = hpo.hpoId
    participant.organizationId = organization.organizationId

    if unconsented is True:
      enrollment_status = None
    elif time_mem is None:
      enrollment_status = EnrollmentStatus.INTERESTED
    elif time_fp is None:
      enrollment_status = EnrollmentStatus.MEMBER
    else:
      enrollment_status = EnrollmentStatus.FULL_PARTICIPANT

    with FakeClock(time_int):
      self.dao.insert(participant)

    participant.providerLink = make_primary_provider_link_for_name(hpo.name)
    with FakeClock(time_mem):
      self.dao.update(participant)

    if enrollment_status is None:
      return None

    summary = self.participant_summary(participant)

    if first_name:
      summary.firstName = first_name
    if last_name:
      summary.lastName = last_name

    if gender_id:
      summary.genderIdentityId = gender_id
    if dob:
      summary.dateOfBirth = dob
    else:
      summary.dateOfBirth = datetime.date(1978, 10, 10)
    if state_id:
      summary.stateId = state_id

    summary.enrollmentStatus = enrollment_status

    summary.enrollmentStatusMemberTime = time_mem
    summary.enrollmentStatusCoreOrderedSampleTime = time_fp
    summary.enrollmentStatusCoreStoredSampleTime = time_fp_stored

    summary.hpoId = hpo.hpoId
    summary.organizationId = organization.organizationId

    if time_study is not None:
      with FakeClock(time_mem):
        summary.consentForStudyEnrollment = QuestionnaireStatus.SUBMITTED
        summary.consentForStudyEnrollmentTime = time_study

    if time_mem is not None:
      with FakeClock(time_mem):
        summary.consentForElectronicHealthRecords = QuestionnaireStatus.SUBMITTED
        summary.consentForElectronicHealthRecordsTime = time_mem

    if time_fp is not None:
      with FakeClock(time_fp):
        if not summary.consentForElectronicHealthRecords:
          summary.consentForElectronicHealthRecords = QuestionnaireStatus.SUBMITTED
          summary.consentForElectronicHealthRecordsTime = time_fp
        summary.questionnaireOnTheBasicsTime = time_fp
        summary.questionnaireOnLifestyleTime = time_fp
        summary.questionnaireOnOverallHealthTime = time_fp
        summary.physicalMeasurementsFinalizedTime = time_fp
        summary.physicalMeasurementsTime = time_fp
        summary.sampleOrderStatus1ED04Time = time_fp
        summary.sampleOrderStatus1SALTime = time_fp
        summary.sampleStatus1ED04Time = time_fp
        summary.sampleStatus1SALTime = time_fp
        summary.biospecimenOrderTime = time_fp
        summary.numCompletedBaselinePPIModules = REQUIRED_PPI_MODULE_COUNT

    self.ps_dao.insert(summary)

    return summary

  def _update_ehr(self, participant_summary, update_time):
    receipt = EhrReceipt(organizationId=participant_summary.organizationId,
                         receiptTime=update_time)
    self.ehr_receipt_dao.insert(receipt)
    self.ps_dao.update_ehr_status(participant_summary, update_time)
    self.ps_dao.update(participant_summary)


class MetricsEhrMultiEndpointTest(MetricsEhrApiTestBase):
  """
  NOTE: as of 2019-03-19, This API's logic is tested through the `combined` endpoint.
  This test case confirms that the `combined` matches the sub-part endpoints.
  """

  def setUp(self, **kwargs):
    super(MetricsEhrMultiEndpointTest, self).setUp(**kwargs)

    #
    # insert some test data
    #
    for date in iter_dates(
      datetime.date(2017, 12, 30),
      datetime.date(2018, 2, 1)
    ):
      calendar_day = Calendar(day=date)
      CalendarDao().insert(calendar_day)
    # noinspection PyArgumentList
    participant_1 = Participant(participantId=1, biobankId=1)
    summary_1 = self._make_participant(
      participant_1, 'Alice', 'Aardvark', self.hpo_foo, self.org_foo_a,
      time_int=datetime.datetime(2018, 1, 2),
      time_mem=datetime.datetime(2018, 1, 3),
      time_study=datetime.datetime(2018, 1, 3),
      time_fp=datetime.datetime(2018, 1, 4)
    )
    self._update_ehr(
      summary_1,
      update_time=datetime.datetime(2018, 1, 5)
    )

    # noinspection PyArgumentList
    participant_2 = Participant(participantId=2, biobankId=2)
    summary_2 = self._make_participant(
      participant_2, 'Bo', 'Badger', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_study=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )
    self._update_ehr(
      summary_2,
      update_time=datetime.datetime(2018, 1, 6)
    )

    # noinspection PyArgumentList
    participant_3 = Participant(participantId=3, biobankId=3)
    self._make_participant(
      participant_3, 'Cheryl', 'Caterpillar', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_study=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )
    participant_3.withdrawalStatus = WithdrawalStatus.NO_USE
    self.dao.update(participant_3)

    # noinspection PyArgumentList
    participant_4 = Participant(participantId=4, biobankId=4)
    self._make_participant(
      participant_4, 'Dan', 'Donkey', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_study=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )
    participant_4.isGhostId = True
    self.dao.update(participant_4)

    # noinspection PyArgumentList
    participant_5 = Participant(participantId=5, biobankId=5)
    self._make_participant(
      participant_5, 'Elia', 'Elephant', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_study=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )

    # noinspection PyArgumentList
    participant_6 = Participant(participantId=6, biobankId=6)
    self._make_participant(
      participant_6, 'Elia', 'Elephant', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )

  def test_combined_endpoint_matches_parts(self):
    combined_response = self.send_get('MetricsEHR')
    participants_over_time_response = self.send_get(
      'MetricsEHR/ParticipantsOverTime',
    )
    organizations_response = self.send_get(
      'MetricsEHR/Organizations',
    )
    self.assertEqual(3, participants_over_time_response['EHR_CONSENTED'])
    self.assertEqual(2, participants_over_time_response['EHR_RECEIVED'])
    self.assertEqual(combined_response['metrics'], participants_over_time_response)
    self.assertEqual(combined_response['organization_metrics'], organizations_response)


class MetricsEhrApiTest(MetricsEhrApiTestBase):

  def test_consented_counts(self):
    # Set up data
    for date in iter_dates(
      datetime.date(2017, 12, 30),
      datetime.date(2018, 2, 1)
    ):
      calendar_day = Calendar(day=date)
      CalendarDao().insert(calendar_day)

    # noinspection PyArgumentList
    participant_1 = Participant(participantId=1, biobankId=4)
    self._make_participant(
      participant_1, 'Alice', 'Aardvark', self.hpo_foo, self.org_foo_a,
      time_int=datetime.datetime(2018, 1, 2),
      time_mem=datetime.datetime(2018, 1, 3),
      time_study=datetime.datetime(2018, 1, 3),
      time_fp=datetime.datetime(2018, 1, 4),
    )

    # noinspection PyArgumentList
    participant_2 = Participant(participantId=2, biobankId=5)
    self._make_participant(
      participant_2, 'Bo', 'Badger', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_study=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )

    # Begin testing
    response = self.send_get('MetricsEHR')
    self.assertEqual(response['metrics']['EHR_CONSENTED'], 2)
    self.assertEqual(
      response['metrics']['EHR_CONSENTED'],
      sum([o['total_ehr_consented'] for o in response['organization_metrics'].values()])
    )

    # test with organization filtering
    response = self.send_get('MetricsEHR', query_string=urllib.urlencode({
      'organization': 'foo_a',
    }))
    self.assertEqual(response['metrics']['EHR_CONSENTED'], 1)
    self.assertEqual(
      response['metrics']['EHR_CONSENTED'],
      sum([o['total_ehr_consented'] for o in response['organization_metrics'].values()])
    )


  def test_received_counts(self):
    # Set up data
    for date in iter_dates(
      datetime.date(2017, 12, 30),
      datetime.date(2018, 2, 1)
    ):
      calendar_day = Calendar(day=date)
      CalendarDao().insert(calendar_day)

    # noinspection PyArgumentList
    participant_1 = Participant(participantId=1, biobankId=4)
    summary_1 = self._make_participant(
      participant_1, 'Alice', 'Aardvark', self.hpo_foo, self.org_foo_a,
      time_int=datetime.datetime(2018, 1, 2),
      time_mem=datetime.datetime(2018, 1, 3),
      time_study=datetime.datetime(2018, 1, 3),
      time_fp=datetime.datetime(2018, 1, 4)
    )

    self._update_ehr(summary_1, update_time=datetime.datetime(2018, 1, 5))
    response = self.send_get('MetricsEHR')
    self.assertEqual(response['metrics']['EHR_RECEIVED'], 1)
    self.assertEqual(
      response['metrics']['EHR_RECEIVED'],
      sum([o['total_ehr_data_received'] for o in response['organization_metrics'].values()])
    )

    # noinspection PyArgumentList
    participant_2 = Participant(participantId=2, biobankId=5)
    summary_2 = self._make_participant(
      participant_2, 'Bo', 'Badger', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_study=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )

    self._update_ehr(summary_2, update_time=datetime.datetime(2018, 1, 6))
    response = self.send_get('MetricsEHR')
    self.assertEqual(response['metrics']['EHR_RECEIVED'], 2)
    self.assertEqual(
      response['metrics']['EHR_RECEIVED'],
      sum([o['total_ehr_data_received'] for o in response['organization_metrics'].values()])
    )

    # participant with EHR but no consent
    participant_3 = Participant(participantId=3, biobankId=6)
    summary_3 = self._make_participant(
      participant_3, 'Bo', 'Badger', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4)
    )
    self._update_ehr(summary_3, update_time=datetime.datetime(2018, 1, 6))

    response = self.send_get('MetricsEHR')
    self.assertEqual(response['metrics']['EHR_RECEIVED'], 2)
    self.assertEqual(
      response['metrics']['EHR_RECEIVED'],
      sum([o['total_ehr_data_received'] for o in response['organization_metrics'].values()])
    )

    # test with organization filtering
    response = self.send_get('MetricsEHR', query_string=urllib.urlencode({
      'organization': 'FOO_A',
    }))
    self.assertEqual(response['metrics']['EHR_RECEIVED'], 1)
    self.assertEqual(
      response['metrics']['EHR_RECEIVED'],
      sum([o['total_ehr_data_received'] for o in response['organization_metrics'].values()])
    )


class MetricsEhrApiOrganizationTest(MetricsEhrApiTestBase):

  def test_cutoff_date_filtering(self):
    # noinspection PyArgumentList
    participant_1 = Participant(participantId=1, biobankId=4)
    summary_1 = self._make_participant(
      participant_1, 'A', 'Aardvark', self.hpo_foo, self.org_foo_a,
      time_int=datetime.datetime(2018, 1, 1),
      time_study=datetime.datetime(2018, 1, 2),
      time_mem=datetime.datetime(2018, 1, 3),
      time_fp=datetime.datetime(2018, 1, 4)
    )

    # noinspection PyArgumentList
    participant_2 = Participant(participantId=2, biobankId=5)
    summary_2 = self._make_participant(
      participant_2, 'B', 'Badger', self.hpo_foo, self.org_foo_a,
      time_int=datetime.datetime(2018, 1, 2),
      time_study=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )

    # noinspection PyArgumentList
    participant_3 = Participant(participantId=3, biobankId=6)
    summary_3 = self._make_participant(
      participant_3, 'C', 'Chicken', self.hpo_bar, self.org_bar_a,
      time_int=datetime.datetime(2018, 1, 2),
      time_study=datetime.datetime(2018, 1, 3),
      time_mem=datetime.datetime(2018, 1, 4),
      time_fp=datetime.datetime(2018, 1, 5)
    )

    for summary in [summary_1]:
      self._update_ehr(summary, update_time=datetime.datetime(2018, 1, 5))

    for summary in [summary_2, summary_3]:
      self._update_ehr(summary, update_time=datetime.datetime(2018, 1, 6))

    # Begin testing
    response = self.send_get('MetricsEHR/Organizations', query_string=urllib.urlencode({
      'end_date': '2018-01-01',
      'interval': 'day'
    }))
    self.assertEqual(
      response[str(self.org_foo_a.externalId)],
      {
        u'organization_id': self.org_foo_a.externalId,
        u'organization_name': unicode(self.org_foo_a.displayName),
        u'total_participants': 1,
        u'total_primary_consented': 0,
        u'total_ehr_consented': 0,
        u'total_core_participants': 0,
        u'total_ehr_data_received': 0,
        u'last_ehr_submission_date': u'2018-01-06',
      }
    )
    self.assertEqual(
      response[str(self.org_bar_a.externalId)],
      {
        u'organization_id': self.org_bar_a.externalId,
        u'organization_name': unicode(self.org_bar_a.displayName),
        u'total_participants': 0,
        u'total_primary_consented': 0,
        u'total_ehr_consented': 0,
        u'total_core_participants': 0,
        u'total_ehr_data_received': 0,
        u'last_ehr_submission_date': u'2018-01-06',
      }
    )

    response = self.send_get('MetricsEHR/Organizations', query_string=urllib.urlencode({
      'end_date': '2018-01-02',
      'interval': 'day'
    }))
    self.assertEqual(
      response[str(self.org_foo_a.externalId)],
      {
        u'organization_id': self.org_foo_a.externalId,
        u'organization_name': unicode(self.org_foo_a.displayName),
        u'total_participants': 2,
        u'total_primary_consented': 1,
        u'total_ehr_consented': 0,
        u'total_core_participants': 0,
        u'total_ehr_data_received': 0,
        u'last_ehr_submission_date': u'2018-01-06',
      }
    )

    response = self.send_get('MetricsEHR/Organizations', query_string=urllib.urlencode({
      'end_date': '2018-01-03',
      'interval': 'day'
    }))
    self.assertEqual(
      response[str(self.org_foo_a.externalId)],
      {
        u'organization_id': self.org_foo_a.externalId,
        u'organization_name': unicode(self.org_foo_a.displayName),
        u'total_participants': 2,
        u'total_primary_consented': 2,
        u'total_ehr_consented': 1,
        u'total_core_participants': 0,
        u'total_ehr_data_received': 0,
        u'last_ehr_submission_date': u'2018-01-06',
      }
    )

    response = self.send_get('MetricsEHR/Organizations', query_string=urllib.urlencode({
      'end_date': '2018-01-04',
      'interval': 'day'
    }))
    self.assertEqual(
      response[str(self.org_foo_a.externalId)],
      {
        u'organization_id': self.org_foo_a.externalId,
        u'organization_name': unicode(self.org_foo_a.displayName),
        u'total_participants': 2,
        u'total_primary_consented': 2,
        u'total_ehr_consented': 2,
        u'total_core_participants': 1,
        u'total_ehr_data_received': 0,
        u'last_ehr_submission_date': u'2018-01-06',
      }
    )

    response = self.send_get('MetricsEHR/Organizations', query_string=urllib.urlencode({
      'end_date': '2018-01-05',
      'interval': 'day'
    }))
    self.assertEqual(
      response[str(self.org_foo_a.externalId)],
      {
        u'organization_id': self.org_foo_a.externalId,
        u'organization_name': unicode(self.org_foo_a.displayName),
        u'total_participants': 2,
        u'total_primary_consented': 2,
        u'total_ehr_consented': 2,
        u'total_core_participants': 2,
        u'total_ehr_data_received': 1,
        u'last_ehr_submission_date': u'2018-01-06',
      }
    )

    response = self.send_get('MetricsEHR/Organizations', query_string=urllib.urlencode({
      'end_date': '2018-01-06',
      'interval': 'day'
    }))
    self.assertEqual(
      response[str(self.org_foo_a.externalId)],
      {
        u'organization_id': self.org_foo_a.externalId,
        u'organization_name': unicode(self.org_foo_a.displayName),
        u'total_participants': 2,
        u'total_primary_consented': 2,
        u'total_ehr_consented': 2,
        u'total_core_participants': 2,
        u'total_ehr_data_received': 2,
        u'last_ehr_submission_date': u'2018-01-06',
      }
    )
