from django.contrib.auth.models import User

from namespace.models import NameSpace, NameSpaceMember
from samatha.exceptions import BusinessError
from samatha.services import UserActivityService, SuperService
from samatha.validator import InputValidator


class CreateNameSpaceService(UserActivityService):
    input_validator = InputValidator()

    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return

    def _do_service(self, name=None, key=None, desc=None):
        self.input_validator.validate_require_parameter(name=name, key=key)
        self.input_validator.validate_not_too_long_parameter(key=key, max_len=8)
        namespace = NameSpace(name=name, key=key, desc=desc,creator=self.user)
        namespace.save()
        return namespace


class AddUserToNameSpaceService(UserActivityService):
    input_validator = InputValidator()

    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return

    def _do_service(self, user_email=None, role_key=NameSpaceMember.ROLE_MEMBER, namespace=None):
        self.input_validator.validate_require_parameter(user_email=user_email, role_key=role_key)
        if User.objects.filter(email = user_email).exists():
            user_obj = User.objects.get(email = user_email)
        else:
            user_obj = SuperService().create_user(email=user_email)
        if not NameSpaceMember.objects.filter(member=user_obj).exists():
            nm = NameSpaceMember(member=user_obj, namespace=namespace,creator=self.user)
            nm.add_role(role_key)
            nm.save()
        else:
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name=k, reason_desc="Value is None")
        return nm
