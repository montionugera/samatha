import uuid

from django.test import TestCase

from epic.tests import _add_epic, BaseEpicTestCase
from sprint.services import CreateSprintService


class BaseSprintTestCase(BaseEpicTestCase):
    pass


class ManageSprintTestCase(BaseSprintTestCase):

    def test_user_can_create_sprint(self):
        sprint_service = CreateSprintService(user=self.user)
        name_space = self.namespace
        sprint_slot = sprint_service.do_service(name_space=name_space)
        self.assertIsNotNone(sprint_slot)

