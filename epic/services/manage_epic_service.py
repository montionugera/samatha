from django.contrib.auth.models import User

from epic.models import Epic, Story, Task, EpicMember, EpicSpec
from namespace.models import NameSpaceMember
from samatha.exceptions import BusinessError
from samatha.services import UserActivityService, SuperService
from samatha.validator import InputValidator


# superadmin__create_namespace
# superadmin_or_name_space_owner__invite_user_to_join_namespace

# namespace_owner/board/owner__create/update_draft_epic
# namespace_owner__update_epic_state_to_todo_state + epicmanager

# epicmanager assign epic's role
# epicmanager/ba add story to epic
# epicmanager/ba add spec to epic

# sa perform task breakdown

# task's responder move task to current sprint

# task's developer move task state to to-do (every field complete)
# task's developer move task state to In-progress
# task's developer move task state to To-verify

# epic's tester create TestSuite
# epic's tester perform testcase breakdown
# epic's tester create TestRound
# epic's tester add Testcase to TestRound
# epic's tester record TestRecord
# epic's tester generate Defect for TestRound
# epic's tester system move task state to Test-fail

# reporter create DefectReport
# epicmanager fullfill defectReport Tester/Developer/Task


class CreateEpicService(UserActivityService):
    def _do_service(self, epic_key=None, epic_name=None, epic_desc=None, namespace=None, manager=None):
        self.input_validator.validate_require_parameter(epic_key=epic_key, epic_name=epic_name
                                                        , manager=manager)
        self.input_validator.validate_not_too_long_parameter(epic_key=epic_key, epic_name=epic_name)
        if Epic.objects.filter(key=epic_key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='epic_key',
                reason_desc="This key already exist ")
        epic = Epic(key=epic_key, name=epic_name, desc=epic_desc, namespace=namespace,
                    creator=self.user)
        epic.save()

        sv = LinkUnlinkUserToEpicService(self.user)
        sv._do_service(user_email=manager.email, role_key=EpicMember.ROLE_MANAGER, epic=epic)

        return epic


class UpdateEpicService(UserActivityService):
    def _do_service(self, epic_key=None, epic_name=None, epic_desc=None):
        self.input_validator.validate_require_parameter(epic_key=epic_key, epic_name=epic_name)
        self.input_validator.validate_not_too_long_parameter(epic_name=epic_name)
        if not Epic.objects.filter(key=epic_key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='epic_key',
                reason_desc="This key not exist ")

        epic = Epic.objects.get(key=epic_key)
        epic.name = epic_name
        epic.desc = epic_desc
        epic.save()

        return epic


class LinkUnlinkUserToEpicService(UserActivityService):
    CMD_LINK = 1
    CMD_REMOVE_ROLE = 0

    def _do_service(self, cmd=
    CMD_LINK, user_email=None, role_key=EpicMember.ROLE_MANAGER, epic=None):
        self.input_validator.validate_require_parameter(user_email=user_email, role_key=role_key,
                                                        epic=epic)
        if User.objects.filter(email=user_email).exists():
            user_obj = User.objects.get(email=user_email)
        else:
            user_obj = SuperService().create_user(email=user_email)
        if not EpicMember.objects.filter(member=user_obj).exists():
            em = EpicMember(member=user_obj, epic=epic, creator=self.user)
        else:
            em = EpicMember.objects.get(member=user_obj)
        if cmd == LinkUnlinkUserToEpicService.CMD_LINK:
            em.add_role(role_key)
        else:
            em.add_role(role_key)
        em.save()
        return em


class AddSpecToEpicService(UserActivityService):
    def _do_service(self, epic=None, story=None, name=None, spec_type=EpicSpec.TYPE_USECASE, spec_data=None):
        self.input_validator.validate_require_parameter(name=name, spec_type=spec_type, spec_data=spec_data)
        epicspec = EpicSpec(epic=epic, name=name, spec_type=spec_type,
                            creator=self.user)
        epicspec.update_data(spec_data)
        epicspec.save()

        return epicspec
