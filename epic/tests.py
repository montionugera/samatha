import uuid
from django.test import TestCase
from epic.models import Epic, Story, Task, EpicSpec, EpicMember
from epic.services.manage_epic_service import CreateEpicService, UpdateEpicService, AddSpecToEpicService, \
    LinkUnlinkUserToEpicService
from epic.services.manage_story_service import CreateStoryService, UpdateStoryService
from epic.services.manage_task_service import UpdateTaskInfoService, CreateTaskService, UpdateTaskStateService

from namespace.models import NameSpace
from namespace.tests import _create_namespace
from samatha.services import SuperService
from sprint.services import CreateSprintService


def _add_story(user, epic):
    the_uuid = str(uuid.uuid4())
    epic_service = CreateStoryService(user=user)
    story = epic_service.do_service(epic=epic,
                                    story_key=the_uuid,
                                    story_name=the_uuid + "-name",
                                    story_desc=the_uuid + "-desc")
    return story


def _add_epic(user, namespace):
    the_uuid = str(uuid.uuid4())

    epic_service = CreateEpicService(user=user)
    epic = epic_service.do_service(epic_key=the_uuid,
                                   epic_name=the_uuid + "-name",
                                   epic_desc=the_uuid + "-desc",
                                   namespace=namespace,
                                   manager=user)
    return epic


def _add_task(user, story,epic=None):
    the_uuid = str(uuid.uuid4())
    sv = CreateTaskService(user=user)
    task = sv.do_service(story=story,
                         task_key=the_uuid,
                         task_name=the_uuid + "-name",
                         task_desc=the_uuid + "-desc",
                         task_estimate_hr=3.1,
                         responder=user,
                         epic=epic)
    return task


class BaseEpicTestCase(TestCase):
    def setUp(self):
        # user
        self.user = SuperService().create_user(email='montionugera@gmail.com')
        self.po = SuperService().create_user(email='montionugera+po@gmail.com',is_superuser=False)

        self.epic_developer = SuperService().create_user(email='montionugera+dev@gmail.com',is_superuser=False)
        self.epic_designer = SuperService().create_user(email='montionugera+ds@gmail.com',is_superuser=False)
        self.epic_tester = SuperService().create_user(email='montionugera+test@gmail.com',is_superuser=False)
        self.epic_manager = SuperService().create_user(email='montionugera+manager@gmail.com',is_superuser=False)
        self.epic_sa = SuperService().create_user(email='montionugera+sa@gmail.com',is_superuser=False)
        self.epic_scrummaster = SuperService().create_user(email='montionugera+scrummaster@gmail.com',is_superuser=False)

        self.namespace = NameSpace(name='SPN', creator=self.user)
        self.namespace.save()
        self.epic = _add_epic(self.user, self.namespace)
        self.devmembers = []
        self.devmembers.append(self.epic_developer)
        self.devmembers.append(self.epic_tester)
        self.devmembers.append(self.epic_sa)
        self.devmembers.append(self.epic_scrummaster)

        sprint_service = CreateSprintService(user=self.user)
        name_space = self.namespace
        self.sprint_slot = sprint_service.do_service(name_space=name_space)

    def _add_team_to_ns(self):
        sv = LinkUnlinkUserToEpicService(user=self.user)
        _ = sv.do_service(user_email=self.epic_manager.email, role_key=EpicMember.ROLE_MANAGER, epic=self.epic)

        sv = LinkUnlinkUserToEpicService(user=self.epic_manager)
        _ = sv.do_service(user_email=self.epic_developer.email, role_key=EpicMember.ROLE_DEV, epic=self.epic)
        _ = sv.do_service(user_email=self.epic_tester.email, role_key=EpicMember.ROLE_TEST, epic=self.epic)
        _ = sv.do_service(user_email=self.epic_designer.email, role_key=EpicMember.ROLE_DESIGNER, epic=self.epic)
        _ = sv.do_service(user_email=self.epic_manager.email, role_key=EpicMember.ROLE_DEV, epic=self.epic)


class ManageEpicTestCase(BaseEpicTestCase):
    def test_user_can_add_epic(self):
        epic = _add_epic(self.user, self.namespace)
        self.assertIsNotNone(epic.id)

    def test_user_can_update_epic(self):
        epic = _add_epic(self.user, self.namespace)
        previous_key = epic.key
        the_uuid = str(uuid.uuid4())
        epic_service = UpdateEpicService(user=self.user)
        epic = epic_service.do_service(epic_key=epic.key,
                                       epic_name=the_uuid + "-name",
                                       epic_desc=the_uuid + "-desc")

        self.assertEqual(epic.key, previous_key)
        self.assertEqual(epic.name, the_uuid + "-name")
        self.assertEqual(epic.desc, the_uuid + "-desc")

    def test_epic_manager_can_set_epic_member(self):
        epic = _add_epic(self.user, self.namespace)
        previous_key = epic.key
        the_uuid = str(uuid.uuid4())
        epic_service = UpdateEpicService(user=self.user)
        epic = epic_service.do_service(epic_key=epic.key,
                                       epic_name=the_uuid + "-name",
                                       epic_desc=the_uuid + "-desc")

        self.assertEqual(epic.key, previous_key)
        self.assertEqual(epic.name, the_uuid + "-name")
        self.assertEqual(epic.desc, the_uuid + "-desc")


class ManageStoryTestCase(BaseEpicTestCase):
    def test_user_can_add_new_story_to_epic(self):
        epic = _add_epic(self.user, self.namespace)
        story = _add_story(self.user, epic)
        self.assertIsNotNone(story.id)
        self.assertIsNotNone(story.epic.id)

    def test_user_can_update_story(self):
        epic = _add_epic(self.user, self.namespace)
        epic2 = _add_epic(self.user, self.namespace)
        story = _add_story(self.user, epic)
        the_uuid = str(uuid.uuid4())
        service = UpdateStoryService(user=self.user)
        story2 = service.do_service(epic=epic2,
                                    story_key=story.key,
                                    story_name=the_uuid + "-name",
                                    story_desc=the_uuid + "-desc")

        self.assertEqual(story.id, story2.id)
        self.assertEqual(story.key, story2.key)
        self.assertEqual(story2.name, the_uuid + "-name")
        self.assertEqual(story2.desc, the_uuid + "-desc")


class ManageSpecTestCase(BaseEpicTestCase):
    def test_epic_member_can_add_spec_to_epic(self):
        the_uuid = str(uuid.uuid4())
        service = AddSpecToEpicService(user=self.epic_designer)
        spec = service.do_service(epic=self.epic, name="spec-%s" % the_uuid,
                                  spec_type=EpicSpec.TYPE_USECASE,
                                  spec_data={})

        self.assertIsNotNone(spec.id)

        story = _add_story(self.epic_manager, self.epic)
        spec.relate_stories.add(story)
        spec = EpicSpec.objects.get(id=spec.id)
        self.assertEqual(spec.relate_stories.all().count(), 1)


class ManageTaskTestCase(BaseEpicTestCase):
    def setUp(self):
        super(ManageTaskTestCase, self).setUp()
        self._add_team_to_ns()

    def test_user_can_add_new_task_to_story(self):
        epic = _add_epic(self.user, self.namespace)
        story = _add_story(self.user, epic)
        task = _add_task(self.user, story,epic=story.epic)

        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.story.id)

    def test_user_can_update_task_info(self):
        story = _add_story(self.user, self.epic)
        story2 = _add_story(self.user, self.epic)
        task = _add_task(self.user, story,epic=story.epic)
        the_uuid = str(uuid.uuid4())
        service = UpdateTaskInfoService(user=self.user)
        task2 = service.do_service(story=story2,
                                    task_key=task.key,
                                    task_name=the_uuid + "-name",
                                    task_desc=the_uuid + "-desc",
                                    task_estimate_hr=8.0,
                                    task_sprint_no=35)

        self.assertEqual(task.id, task2.id)
        self.assertEqual(task.key, task2.key)
        self.assertEqual(task2.name, the_uuid + "-name")
        self.assertEqual(task2.desc, the_uuid + "-desc")
        self.assertEqual(task2.estimate_hr, 8.0)
        self.assertEqual(task2.sprint_no, 35)


    def test_task_responder_can_update_task_state_though_verify(self):
        story = _add_story(self.user, self.epic)
        task = _add_task(self.epic_developer, story,epic=story.epic)

        service = UpdateTaskStateService(user=task.responder)
        self.assertEqual(task.task_state, Task.STATE_PREPARE)
        task = service.do_service(task=task, task_state=Task.STATE_TODO)
        task = service.do_service(task=task, task_state=Task.STATE_INPROGRESS)
        task = service.do_service(task=task, task_state=Task.STATE_TOVERIFY)
        task = Task.objects.get(id=task.id)
        self.assertEqual(task.task_state, Task.STATE_TOVERIFY)

    def test_epic_tester_can_update_task_state_through_done(self):
        story = _add_story(self.user, self.epic)
        task = _add_task(self.epic_developer, story,epic=story.epic)

        servicerep = UpdateTaskStateService(user=task.responder)
        self.assertEqual(task.task_state, Task.STATE_PREPARE)
        task = servicerep.do_service(task=task, task_state=Task.STATE_TODO)
        task = servicerep.do_service(task=task, task_state=Task.STATE_INPROGRESS)
        task = servicerep.do_service(task=task, task_state=Task.STATE_TOVERIFY)

        service = UpdateTaskStateService(user=self.epic_tester)
        task = service.do_service(task=task, task_state=Task.STATE_VERIFYING)
        task = service.do_service(task=task, task_state=Task.STATE_TEST_F)

        task = servicerep.do_service(task=task, task_state=Task.STATE_INPROGRESS)
        task = servicerep.do_service(task=task, task_state=Task.STATE_TOVERIFY)
        task = service.do_service(task=task, task_state=Task.STATE_VERIFYING)
        task = service.do_service(task=task, task_state=Task.STATE_TEST_P)
        task = service.do_service(task=task, task_state=Task.STATE_DONE)

        task = Task.objects.get(id=task.id)
        self.assertEqual(task.task_state, Task.STATE_DONE)
