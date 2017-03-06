from __future__ import unicode_literals

from django.db import models

# Create your models here.
from epic.models import  Story, Epic, Task
from django.contrib.auth.models import User

from samatha.json_data_models import TestableChangableItem, TrackableItem


class EpicTestSuite(models.Model):
    key = models.CharField(max_length=128, unique=True)
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, null=True, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)


class EpicTestCase(TrackableItem, TestableChangableItem):
    name = models.CharField(max_length=256)
    test_steps = models.TextField(default='null')
    expected_results = models.TextField(default='null')
    testsuite = models.ForeignKey(EpicTestSuite)


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
    tester = models.ForeignKey(User, null=True, related_name='tester_testround')
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_DONE,
    )


class TestRecord(TrackableItem):
    testround = models.ForeignKey(TestRound, on_delete=models.CASCADE)
    testcase = models.ForeignKey(EpicTestCase, on_delete=models.CASCADE)
    key = models.CharField(max_length=128, unique=True)

    STATE_W8_TEST = 'W8_TEST'
    STATE_PASS = 'PASS'
    STATE_FAIL = 'FAIL'
    STATE_SKIP = 'SKIP'
    STATE_CHOICES = (
        (STATE_W8_TEST, 'Waiting test'),
        (STATE_PASS, 'Test pass'),
        (STATE_FAIL, 'Test fail'),
        (STATE_SKIP, 'Skip test'),
    )
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_W8_TEST,
    )


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
