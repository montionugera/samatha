from __future__ import unicode_literals

import datetime
from django.contrib.auth.models import User
from django.db import models
from math import floor

from epic.models import Task
from namespace.models import NameSpace
from samatha.json_data_models import JsonDataSupportModel


def get_datetime_now():
    return datetime.datetime.now()

# Create your models here.

class SprintSlot(JsonDataSupportModel):
    namespace = models.ForeignKey(NameSpace)
    sprint_no = models.IntegerField(blank=True, null=True)
    initial_point_size = models.IntegerField(default=0)
    progress_point_size = models.IntegerField(default=0)

    @staticmethod
    def get_or_create_sprint_slot(sprint_no=None, name_space=None):
        if sprint_no is None:
            sprint_no = 36 + floor(floor((datetime.datetime.now() -
                                          datetime.datetime(day=11, month=2, year=2017)
                                          ).days + 0.0) / 14)
        s, created = SprintSlot.objects.get_or_create(namespace=name_space, sprint_no=sprint_no)

        return s


class SprintSlotEvent(models.Model):
    sprint_slot = models.ForeignKey(SprintSlot)
    event_point = models.IntegerField(default=0)

    point = models.IntegerField(default=0)
    point_receiver = models.ForeignKey(User)

    EVENT_TYPE_MV_TASK_IN = 'MV_TSK_IN'
    EVENT_TYPE_MV_TASK_OUT = 'MV_TSK_OUT'
    EVENT_TYPE_TASK_STATE_CHNG = 'TSK_ST_CHG_TO'
    created_dttm = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def req_event_register_did_MV_TASK_IN(task, sprint_slot):
        # pp# to-verify# done# reject-req# reject-ac# reject-na
        pass


class SprintTask(models.Model):
    sprint_slot = models.ForeignKey(SprintSlot)
    task = models.ForeignKey(Task)

    class Meta:
        unique_together = ('sprint_slot', 'task',)

    @staticmethod
    def req_event_register_did_MV_TASK_IN(task, sprint_slot):
        pass
