from __future__ import unicode_literals

from django.db import models
import json

# Create your models here.
from epic.models import Story, Epic, Task
from django.contrib.auth.models import User

from samatha.json_data_models import TestableChangableItem, TrackableItem
from sprint.models import SprintSlot


class EpicTestSuite(TrackableItem):
    key = models.CharField(max_length=128, unique=True)
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, null=True, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)


class EpicTestCase(TrackableItem, TestableChangableItem):
    key = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=256)
    test_steps = models.TextField(default='null')
    expected_results = models.TextField(default='null')
    testsuite = models.ForeignKey(EpicTestSuite)

    STATE_PREPARE = 'PP'
    STATE_DONE = 'DONE'

    STATE_CHOICES = (
        (STATE_PREPARE, 'Prepare'),
        (STATE_DONE, 'Done'),
    )
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_PREPARE,
    )

    def get_test_steps(self):
        if self.test_steps is None:
            return []
        return json.loads(self.test_steps)

    def update_test_steps(self, steps_list=list(), auto_save=False):
        self.test_steps = json.dumps(steps_list)
        if auto_save:
            self.save()

    def get_test_expected_results(self):
        if self.expected_results is None:
            return []
        return json.loads(self.expected_results)

    def update_test_expected_results(self, expected_results_list=list(), auto_save=False):
        self.expected_results = json.dumps(expected_results_list)
        if auto_save:
            self.save()

    def get_relate_developer(self):
        if self.test_steps is None:
            return []
        return json.loads(self.test_steps)


class TestRound(TrackableItem):
    key = models.CharField(max_length=128, unique=True)
    STATE_PREPARE = 'PP'
    STATE_INPROGRESS = 'IP'
    STATE_W8_FOR_REVIEW = 'W8RV'
    STATE_DONE = 'DONE'

    STATE_CHOICES = (
        (STATE_PREPARE, 'Prepare'),
        (STATE_INPROGRESS, 'In-progress'),
        (STATE_W8_FOR_REVIEW, 'Generate Report and waiting review'),
        (STATE_DONE, 'Done'),
    )

    sprint_slot = models.ForeignKey(SprintSlot, related_name='sprintslot_testround')
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_PREPARE,
    )


class TestRecord(TrackableItem):
    testround = models.ForeignKey(TestRound, on_delete=models.CASCADE)
    testcase = models.ForeignKey(EpicTestCase, on_delete=models.CASCADE)

    STATE_W8_TEST = 'W8_TEST'
    STATE_PASS = 'PASS'
    STATE_FAIL = 'FAIL'
    STATE_SKIP = 'SKIP'
    STATE_RECONSIDER = 'RECONS'
    STATE_CHOICES = (
        (STATE_W8_TEST, 'Waiting test'),
        (STATE_PASS, 'Test pass'),
        (STATE_FAIL, 'Test fail'),
        (STATE_SKIP, 'Skip test'),
        (STATE_RECONSIDER, 'Re consider'),
    )
    test_steps = models.TextField(default='null')
    expected_results = models.TextField(default='null')
    test_results = models.TextField(default='null')
    developer_question_or_remark = models.TextField(default='')

    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_W8_TEST,
    )
    developer_state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_W8_TEST,
    )
    developer = models.ForeignKey(User, null=True, related_name='developer_testrecord')


class DefectReport(TrackableItem, TestableChangableItem):
    reporter = models.ForeignKey(User, null=True, related_name='defect_reporter')
    responder = models.ForeignKey(User, null=True, related_name='defect_responder')
    relate_stories = models.ManyToManyField(Story)
    relate_tasks = models.ManyToManyField(Task)

    SEVERITY_CRITICAL = 'CC'
    SEVERITY_MAJOR = 'MJ'
    SEVERITY_MINOR = 'MJ'
    SEVERITY_COSMETIC = 'CM'
    SV_CHOICES = (
        (SEVERITY_CRITICAL, 'CRITICAL'),
        (SEVERITY_MAJOR, 'MAJOR'),
        (SEVERITY_MINOR, 'MINOR'),
        (SEVERITY_COSMETIC, 'COSMETIC'),
    )
    severity = models.CharField(
        max_length=20,
        choices=SV_CHOICES,
        default=SEVERITY_CRITICAL,
    )
    PH_UK = 'UK'
    PH_RQ = 'RQ'
    PH_DESIGN = 'DS'
    PH_CODE = 'CD'
    PH_CHOICES = (
        (PH_UK, 'Unknown'),
        (PH_RQ, 'Phase requirement'),
        (PH_DESIGN, 'Phase design'),
        (PH_CODE, 'Phase code'),
    )
    phase_introduce = models.CharField(
        max_length=20,
        choices=PH_CHOICES,
        default=PH_UK,
    )

    ENV_UAT = 'UAT'
    ENV_PROD = 'PROD'
    ENV_CHOICE = (
        (PH_UK, 'UAT'),
        (ENV_PROD, 'Production'),
    )

    environment = models.CharField(
        max_length=20,
        choices=PH_CHOICES,
        default=ENV_UAT,
    )

    DF_TYPE_NORMAL = 'NM'
    DF_TYPE_ISSUE = 'IS'
    DF_TYPE_CHOICES = (
        (DF_TYPE_NORMAL, 'Normal (in test round)'),
        (DF_TYPE_ISSUE, 'Hot issues (post release)'),
    )
    defect_type = models.CharField(
        max_length=20,
        choices=DF_TYPE_CHOICES,
        default=DF_TYPE_NORMAL,
    )
