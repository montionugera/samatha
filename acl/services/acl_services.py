from samatha.services import UserService


class ACLService(UserService):
    full_permission_data = {  # actions
    }

    def _is_super_user_for_space(self):
        return self.user.is_superuser

    def get_role(self, item):
        if self._is_super_user_for_space():
            return self.full_permission_data

    def get_permission_data(self):
        if self._is_super_user_for_space():
            return self.full_permission_data


class SuperACLService(ACLService):
    full_permission_data = {  # actions
        'C_NEW_NS': True,
    }


class NameSpaceACLService(UserService):
    full_permission_data = {  # actions
        'EDIT_NS__': True,
    }

    def _is_super_user_for_space(self):
        return self.user.is_superuser

    def get_permission_data(self):
        if self._is_super_user_for_space():
            return self.full_permission_data
