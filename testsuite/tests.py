import uuid

from django.test import TestCase
from epic.tests import _add_epic, _add_story, BaseEpicTestCase, _add_task

# Create your tests here.
from testsuite.services import AddEpicTestSuiteToEpicService, CreateTestCaseService, CreateTestRoundService, \
    PrepareTestRecordService


class BaseTestSuiteTestCase(BaseEpicTestCase):
    pass


class ManageTestSuiteTestCase(BaseTestSuiteTestCase):
    def test_tester_can_create_testsuite(self):
        test_suite_service = AddEpicTestSuiteToEpicService(self.epic_tester)
        the_uuid = str(uuid.uuid4())
        ets = test_suite_service.do_service(
            key=the_uuid, epic=self.epic, story=None, task=None
        )
        self.assertIsNotNone(ets)
        the_uuid = str(uuid.uuid4())
        story = _add_story(self.epic_manager, self.epic)
        ets = test_suite_service.do_service(
            key=the_uuid, epic=self.epic, story=story, task=None
        )
        self.assertIsNotNone(ets)
        the_uuid = str(uuid.uuid4())
        task = _add_task(self.epic_developer, story, epic=story.epic)
        ets = test_suite_service.do_service(
            key=the_uuid, epic=self.epic, story=story, task=task
        )
        self.assertIsNotNone(ets)

    def test_tester_can_create_testcase(self):
        test_suite_service = AddEpicTestSuiteToEpicService(self.epic_tester)
        the_uuid = str(uuid.uuid4())
        ets = test_suite_service.do_service(
            key=the_uuid, epic=self.epic, story=None, task=None
        )

        the_uuid = str(uuid.uuid4())
        test_case_service = CreateTestCaseService(self.epic_tester)
        tc = test_case_service.do_service(key=the_uuid, title="do something should success",
                                     test_steps=["do1", "do2"], expected_results=["got 1"],
                                     testsuite=ets)
        self.assertIsNotNone(tc)

    def test_tester_can_create_testround_and_record(self):
        test_suite_service = AddEpicTestSuiteToEpicService(self.epic_tester)
        the_uuid = str(uuid.uuid4())
        ets = test_suite_service.do_service(
            key=the_uuid, epic=self.epic, story=None, task=None
        )

        the_uuid = str(uuid.uuid4())
        test_case_service = CreateTestCaseService(self.epic_tester)
        tc = test_case_service.do_service(key=the_uuid, title="do something should success",
                                     test_steps=["do1", "do2"], expected_results=["got 1"],
                                     testsuite=ets)
        the_uuid = str(uuid.uuid4())
        test_round_service = CreateTestRoundService(self.epic_tester)
        tr = test_round_service.do_service(key=the_uuid,sprint_slot = self.sprint_slot)
        test_record_service = PrepareTestRecordService(self.epic_tester)
        test_record = test_record_service.do_service(testround=tr,testcase = tc)
        self.assertIsNotNone(test_record)



