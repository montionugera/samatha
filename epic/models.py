from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from namespace.models import NameSpace
from samatha.json_data_models import TrackableItem, DevelopAbleContainerStateItem, TestableChangableItem, \
    JsonDataSupportModel, RoleManageSuport

EPIC_WORKING_STATUS_LIST = ['In-Queue', 'Reject', 'Pending', 'Coding', 'W8T@UAT', 'T-PASS@UAT', 'W8T@PROD',
                            'T-PASS@PROD', 'DONE']
EPIC_FINALIZING_REQ_STATUS_LIST = ['']
EPIC_DEFINING_REQ_STATUS_LIST = ['']


def get_item_key(item):
    key = "%s-%s-%s" % (item._meta.app_label, item._meta.object_name, item.id)
    return key


def _get_tupple_name(t_key, t_list):
    return t_key, [t_name for t_key, t_name in t_list][0]


class MessageRoom(TrackableItem):
    ref_event_key = models.CharField(max_length=256)
    ref_item_key = models.CharField(max_length=256)
    name = models.CharField(max_length=128)

    @staticmethod
    def get_room_list(item):
        ref_item_key = get_item_key(item=item)
        return MessageRoom.objects.filter(ref_item_key=ref_item_key)


class Message(TrackableItem):
    message_html = models.TextField(default='null')
    room = models.ForeignKey('epic.MessageRoom')

    class Meta:
        abstract = True


class Epic(TrackableItem, DevelopAbleContainerStateItem, JsonDataSupportModel):
    key = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    icon_url = models.CharField(max_length=256)
    desc = models.TextField(default='null')
    namespace = models.ForeignKey(NameSpace, on_delete=models.CASCADE)

    def _get_working_phase_status(self):
        "Returns working progress status on the epic."
        return 'UNKNOWN'

    def _get_deploy_status(self):
        "Returns working progress status on the epic."
        return 'UNKNOWN'

    def _get_finalizing_requirement_status(self):
        "Returns working progress status on the epic."
        return 'UNKNOWN'

    def _get_pitching_milestone_status(self):
        "Returns working progress status on the epic."
        return 'UNKNOWN'


class EpicMember(TrackableItem, RoleManageSuport):
    epic = models.ForeignKey(Epic)
    member = models.ForeignKey(User)
    ROLE_MANAGER = 'MN'
    ROLE_DESIGNER = 'DS'
    ROLE_DEV = 'DEV'
    ROLE_TEST = 'TEST'
    AVAILABLE_ROLES = [ROLE_MANAGER, ROLE_DESIGNER, ROLE_DEV, ROLE_TEST]


class Story(TrackableItem, DevelopAbleContainerStateItem):
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE, related_name='epic_story')
    key = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    desc = models.TextField(default='null')
    data = models.TextField(default='null')

    class Meta(TrackableItem.Meta):
        db_table = 'story_info'


class Task(TrackableItem):
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, null=True, on_delete=models.CASCADE)
    key = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    desc = models.TextField(default='null')
    data = models.TextField(default='null')

    estimate_hr = models.FloatField(default=1.0)
    sprint_no = models.IntegerField(blank=True, null=True)
    actual_hr = models.FloatField(blank=True, null=True)

    responder = models.ForeignKey(User, null=True, related_name='task_responder')

    STATE_PREPARE = 'PP'

    STATE_TODO = 'TODO'
    STATE_INPROGRESS = 'INP'
    STATE_TOVERIFY = 'TV'
    STATE_VERIFYING = 'VING'
    STATE_TEST_F = 'TEST-F'
    STATE_TEST_P = 'TEST-P'

    STATE_DONE = 'DN'
    STATE_PENDING = 'PD'
    STATE_CANCEL = 'CC'

    TAKS_STATE_CHOICES = (
        (STATE_PREPARE, 'Prepare'),
        (STATE_TODO, 'To-do'),
        (STATE_INPROGRESS, 'In-progress'),
        (STATE_TOVERIFY, 'To-verify'),
        (STATE_VERIFYING, 'To-verify'),
        (STATE_TEST_F, 'Test-fail'),
        (STATE_TEST_P, 'Test-pass'),
        (STATE_DONE, 'Done'),
        (STATE_PENDING, 'Pending'),
        (STATE_CANCEL, 'Cancel'),
    )
    TAKS_STATE_PATHS = {
        STATE_PREPARE: [STATE_PENDING, STATE_CANCEL],
        STATE_TODO: [STATE_PENDING, STATE_CANCEL, STATE_INPROGRESS],
        STATE_INPROGRESS: [STATE_PENDING, STATE_CANCEL, STATE_TOVERIFY],
        STATE_TOVERIFY: [STATE_PENDING, STATE_CANCEL, STATE_VERIFYING],
        STATE_VERIFYING: [STATE_PENDING, STATE_CANCEL, STATE_TEST_P, STATE_TEST_F],
        STATE_TEST_F: [STATE_PENDING, STATE_CANCEL, STATE_TODO, STATE_INPROGRESS],
        STATE_TEST_P: [STATE_PENDING, STATE_CANCEL, STATE_DONE],
        STATE_DONE: [STATE_CANCEL, STATE_TEST_F],
        STATE_PENDING: [STATE_PENDING, STATE_TODO],
        STATE_CANCEL: [STATE_TODO],
    }

    task_state = models.CharField(
        max_length=10,
        choices=TAKS_STATE_CHOICES,
        default=STATE_PREPARE,
    )

    class Meta(TrackableItem.Meta):
        db_table = 'task_info'

    def get_updatable_states_for(self, user):
        current_state = self.task_state
        user.get_epic_roles(self.epic)
        is_responder = (self.responder_id == user.id)
        limit_states = Task.TAKS_STATE_PATHS.get(current_state, [])
        available_states = []
        if is_responder:
            available_states += [Task.STATE_PREPARE, Task.STATE_TODO, Task.STATE_TOVERIFY,
                                 Task.STATE_PENDING, Task.STATE_CANCEL]
        if EpicMember.ROLE_TEST in user.get_epic_roles:
            available_states += [Task.STATE_VERIFYING,
                                 Task.STATE_TEST_F, Task.STATE_TEST_P, Task.STATE_DONE]
        available_states = list(set(available_states).intersection(set(limit_states)))
        print current_state
        print available_states
        return available_states


class EpicSpec(TrackableItem, TestableChangableItem, JsonDataSupportModel):
    epic = models.ForeignKey(Epic, on_delete=models.CASCADE)
    relate_stories = models.ManyToManyField(Story)
    relate_tasks = models.ManyToManyField(Task)
    name = models.CharField(max_length=128)
    TYPE_USECASE = 'UC'
    TYPE_UX_UI = 'UX_UI'
    TYPE_SEQ_DIAGRAM = 'SEQD'
    TYPE_API = 'API'
    SPEC_TYPE_CHOICES = (
        (TYPE_USECASE, 'Usecase'),
        (TYPE_UX_UI, 'UX-UI'),
        (TYPE_SEQ_DIAGRAM, 'Sequence-diagram'),
        (TYPE_API, 'API-Spec'),
        # (TYPE_TEST_SUITE, 'Test-suite'),
    )
    spec_type = models.CharField(
        max_length=10,
        choices=SPEC_TYPE_CHOICES,
        default=TYPE_USECASE,
    )

    class Meta(TrackableItem.Meta):
        db_table = 'spec_info'
