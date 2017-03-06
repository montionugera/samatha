from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from samatha.json_data_models import TrackableItem, JsonDataSupportModel


class NameSpace(TrackableItem):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=8, unique=True)
    desc = models.TextField(default='null')
    data = models.TextField(default='null')


class NameSpaceMember(TrackableItem, JsonDataSupportModel):
    namespace = models.ForeignKey(NameSpace)
    member = models.ForeignKey(User)
    ROLE_MANAGER = 'MANAGER'
    ROLE_BOARD = 'BOARD'
    ROLE_MEMBER = 'MEMBER'
    NAMESPACE_ROLES = [ROLE_MANAGER, ROLE_BOARD, ROLE_MEMBER]

    def get_roles(self):
        roles = self.get_data_json('roles', ['MEMBER'])
        return roles

    def check_role(self, role_key):
        if role_key not in NameSpaceMember.NAMESPACE_ROLES:
            raise Exception("role not in list")

    def add_role(self, role_key):
        self.check_role(role_key)
        roles = self.get_roles()
        roles.append(role_key)
        roles = list(set(roles))
        self.update_data({'roles': roles})
