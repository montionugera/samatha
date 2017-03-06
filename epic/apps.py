from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.auth import get_user_model


class EpicConfig(AppConfig):
    name = 'epic'
    def ready(self):
        # Add some functions to user model:
        def get_epic_roles(self, epic):
            from epic.models import EpicMember
            return EpicMember.objects.get(member=self, epic=epic).get_roles()

        UserModel = get_user_model()
        UserModel.add_to_class('get_epic_roles', get_epic_roles)
