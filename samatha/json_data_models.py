from django.db import models

from django.contrib.auth.models import User


class DevelopAbleContainerStateItem(models.Model):
    STATES_PREPARE = 'PP'
    STATES_READY_FOR_DEV = 'RD-DEV'
    STATE_INPROGRESS = 'INP'
    STATE_DONE = 'DN'
    STATE_CANCEL = 'CC'

    STATE_CHOICES = (
        (STATES_PREPARE, 'PP'),
        (STATES_READY_FOR_DEV, 'Ready-for-dev'),
        (STATE_INPROGRESS, 'In-progress'),
        (STATE_DONE, 'Done'),
        (STATE_CANCEL, 'Cancel'),
    )
    base_state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES,
        default=STATES_PREPARE,
    )

    class Meta:
        abstract = True


class TrackableItem(models.Model):
    created_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User,
                                related_name="%(app_label)s_%(class)s_creator_related",
                                related_query_name="%(app_label)s_%(class)ss_creator", )

    class Meta:
        abstract = True


class TestableChangableItem(models.Model):
    approve_dttm = models.DateTimeField(auto_now_add=True)
    approver = models.ForeignKey(User, null=True,
                                 related_name="%(app_label)s_%(class)s_approver_related",
                                 related_query_name="%(app_label)s_%(class)ss_approver", )

    reject_dttm = models.DateTimeField(auto_now_add=True)
    rejector = models.ForeignKey(User, null=True,
                                 related_name="%(app_label)s_%(class)s_rejector_related",
                                 related_query_name="%(app_label)s_%(class)ss_rejector", )
    STATE_PREPARE = 'PP'
    STATE_REQ_APPROVE = 'RQ_APP'
    STATE_REQ_APPROVE_REJECT_ASK = 'RQ_APP_RJ_ASK'
    STATE_REQ_APPROVE_REJECT_ACCEPT = 'RQ_APP_RJ_AC'
    STATE_REQ_APPROVE_REJECT_NOT_ACCEPT = 'RQ_APP_RJ_NOT-AC'
    STATE_APPROVED = 'APPV'
    STATE_CHG = 'CHG_PP'

    STATE_CHOICES = (
        (STATE_PREPARE, 'Prepare'),
        (STATE_REQ_APPROVE, 'Request for approve'),
        (STATE_REQ_APPROVE_REJECT_ASK, 'Reject ask'),
        (STATE_REQ_APPROVE_REJECT_ACCEPT, 'Reject accepted'),
        (STATE_REQ_APPROVE_REJECT_NOT_ACCEPT, 'Reject not accepted'),
        (STATE_APPROVED, 'Approved'),
        (STATE_CHG, 'Change prepare'),
    )
    approve_state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_PREPARE,
    )

    class Meta:
        abstract = True

    def get_change_status_list_available(self):
        state_keys = []
        if self.item_state in [TestableChangableItem.STATE_DRAFT,
                               TestableChangableItem.STATE_CHG]:  # Draft
            state_keys.append(TestableChangableItem.STATE_REQ_APPROVE)
        elif self.item_state in [TestableChangableItem.STATE_REQ_APPROVE]:  # REQ
            state_keys.append(TestableChangableItem.STATE_REQ_APPROVE_REJECT_ASK)
            state_keys.append(TestableChangableItem.STATE_APPROVED)
        elif self.item_state in [TestableChangableItem.STATE_REQ_APPROVE_REJECT_ASK]:  # REJ
            state_keys.append(TestableChangableItem.STATE_REQ_APPROVE_REJECT_ACCEPT)
            state_keys.append(TestableChangableItem.STATE_REQ_APPROVE_REJECT_NOT_ACCEPT)
        elif self.item_state in [TestableChangableItem.STATE_REQ_APPROVE_REJECT_ACCEPT]:  # REJ-A
            state_keys.append(TestableChangableItem.STATE_REQ_APPROVE)
            state_keys.append(TestableChangableItem.STATE_CHG)
        elif self.item_state in [TestableChangableItem.STATE_REQ_APPROVE_REJECT_NOT_ACCEPT]:  # REJ-N-A
            state_keys.append(TestableChangableItem.STATE_REQ_APPROVE_REJECT_ASK)
            state_keys.append(TestableChangableItem.STATE_APPROVED)
        elif self.item_state in [TestableChangableItem.STATE_APPROVED]:  # APP
            state_keys.append(TestableChangableItem.STATE_CHG)
        state_keys = list(set(state_keys))

        from epic.models import _get_tupple_name
        return [{'state_val': state_key,
                 'state_display': _get_tupple_name(state_key, TestableChangableItem.STATE_CHOICES)}
                for state_key in state_keys]

    def is_editable(self, user_role_code):
        return True


class DevelopAbleItem(models.Model):
    STATE_SKIP = 'SKP'
    STATE_PEND = 'PEND'
    STATE_READY = 'RD'
    STATE_INPROGRESS = 'INP'
    STATE_ON_UAT = 'ON_UAT'
    STATE_ON_PROD = 'ON_PROD'

    STATE_CHOICES = (
        (STATE_SKIP, 'Skip'),
        (STATE_PEND, 'Pending'),
        (STATE_READY, 'Ready-for-develop'),
        (STATE_INPROGRESS, 'In-progress'),
        (STATE_ON_UAT, 'Deployed-on-UAT'),
        (STATE_ON_PROD, 'Deployed-on-Production'),
    )
    dev_state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_SKIP,
    )

    class Meta:
        abstract = True


class JsonDataSupportModel(models.Model):
    data = models.TextField(default='null')

    class Meta:
        abstract = True

    def _validate_data(self, data_dict):
        pass

    def update_data(self, data_dict):
        import json
        self._validate_data(data_dict)
        current_data_dict = self.get_data_json()
        if type(current_data_dict) == type(None):
            current_data_dict = {}
        current_data_dict.update(data_dict)
        self.data_json = current_data_dict
        self.data = json.dumps(current_data_dict)
        return self.data_json

    def get_data_json(self, key=None, default=None):
        import json

        try:
            type(self.data_json)
        except:
            try:
                self.data_json = json.loads(self.data)
                if self.data_json is None:
                    self.data_json = {}
            except:
                self.data_json = {}

        if key is not None:
            if key in self.data_json:
                return self.data_json[key]
            else:
                return default
        return self.data_json

class RoleManageSuport(JsonDataSupportModel):
    AVAILABLE_ROLES = []
    class Meta:
        abstract = True

    def get_roles(self):
        roles = self.get_data_json('roles', ['MEMBER'])
        return roles

    def check_role(self, role_key):
        if role_key not in self.AVAILABLE_ROLES:
            raise Exception("role not in list")

    def add_role(self, role_key):
        self.check_role(role_key)
        roles = self.get_roles()
        roles.append(role_key)
        roles = list(set(roles))
        self.update_data({'roles': roles})