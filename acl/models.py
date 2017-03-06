from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Acl(models.Model):

    user = models.ForeignKey(User)
    data = models.TextField(default='null')
    ACL_LEVEL_SUPER = 'S'
    ACL_LEVEL_NAME_SPACE = 'NS'
    ACL_LEVEL_EPIC = 'E'
    ACL_LEVEL_STORY = 'ST'
    ACL_LEVEL_TASK = 'T'
    ACL_LEVEL_CHOICES = (
        (ACL_LEVEL_SUPER, 'Super'),
        (ACL_LEVEL_NAME_SPACE, 'Namespace'),
        (ACL_LEVEL_EPIC, 'Epic'),
        (ACL_LEVEL_STORY, 'Story'),
        (ACL_LEVEL_TASK, 'Task'),
    )
    level = models.CharField(
        max_length=2,
        choices=ACL_LEVEL_CHOICES,
    )
    created_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)

