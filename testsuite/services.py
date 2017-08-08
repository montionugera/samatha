from samatha.exceptions import BusinessError
from testsuite.models import EpicTestSuite, EpicTestCase, TestRound, TestRecord
from samatha.services import UserActivityService


class AddEpicTestSuiteToEpicService(UserActivityService):
    def _do_service(self, key=None, epic=None, story=None, task=None):
        self.input_validator.validate_require_parameter(key=key, epic=epic)
        if EpicTestSuite.objects.filter(key=key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='test_suite_key',
                reason_desc="This key(%s) already exist " % key)
        else:
            ets = EpicTestSuite(key=key, epic=epic, story=story, task=task,
                                creator=self.user)
            ets.save()

        return ets


class CreateTestCaseService(UserActivityService):
    def _do_service(self, key=None, title=None, test_steps=None, expected_results=None, testsuite=None):
        self.input_validator.validate_require_parameter(key=key, title=title, test_steps=test_steps,
                                                        expected_results=expected_results,
                                                        testsuite=testsuite)
        self.input_validator.validate_shuoud_be_list_parameter(test_steps=test_steps,
                                                               expected_results=expected_results, )
        if EpicTestCase.objects.filter(key=key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='test_case_key',
                reason_desc="This key(%s) already exist " % key)
        else:
            e_test_case = EpicTestCase(key=key, testsuite=testsuite, title=title,
                                       creator=self.user)
            e_test_case.update_test_expected_results(expected_results)
            e_test_case.update_test_steps(test_steps)
            e_test_case.save()

        return e_test_case


class CreateTestRoundService(UserActivityService):
    def _do_service(self, key=None, sprint_slot = None):
        self.input_validator.validate_require_parameter(key=key,sprint_slot = sprint_slot)
        if TestRound.objects.filter(key=key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='test_round_key',
                reason_desc="This key(%s) already exist " % key)
        else:
            test_round = TestRound(key=key, sprint_slot=sprint_slot,
                                   creator=self.user)
            test_round.save()
        return test_round


class PrepareTestRecordService(UserActivityService):

    def _do_service(self, testround=None, testcase=None):
        self.input_validator.validate_require_parameter(testround=testround,
                                                        testcase=testcase)
        if TestRecord.objects.filter(testround=testround, testcase=testcase).exists():
            return TestRecord.objects.get(testround=testround, testcase=testcase)
        else:
            test_record = TestRecord(testround=testround, testcase=testcase,
                                   creator=self.user)
            test_record.save()
        return test_record
