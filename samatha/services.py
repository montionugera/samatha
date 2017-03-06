from django.contrib.auth.models import User

from samatha.validator import InputValidator


class UserService(object):
    def __init__(self, user):
        assert isinstance(user, User)
        self.user = user


class UserActivityService(UserService):
    input_validator = InputValidator()
    activity_key = None

    def _is_super_admin(self):
        return self.user.is_superuser

    def _did_user_perform_activity_success(self, obj=None):
        pass

    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return

    def do_service(self, **kwargs):
        self._check_can_do(**kwargs)
        obj = self._do_service(**kwargs)
        self._did_user_perform_activity_success(obj=obj)
        return obj

    def _do_service(self, **kwargs):
        raise NotImplementedError()
        return obj


class SuperService(object):
    def create_user(self, email, password='qwerty', is_superuser=False):
        username = email
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username, email, password, is_superuser=is_superuser)
        else:
            user = User.objects.get(email=email)
        return user
