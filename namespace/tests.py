from django.test import TestCase

# Create your tests here.
from namespace.models import NameSpaceMember
from namespace.services.manage_namespace_service import CreateNameSpaceService, AddUserToNameSpaceService
from samatha.services import SuperService


def _create_namespace(super_user):
    s = CreateNameSpaceService(user=super_user)
    ns = s.do_service(name='shoppening', key='SPN', desc="Shoppening team yeah!")

    return ns


class ManageNameSpaceTestCase(TestCase):
    def setUp(self):
        # user
        self.super_user = SuperService().create_user(email='montionugera@gmail.com')
        self.uuids = []

    def test_user_can_create_namespace(self):
        ns = _create_namespace(self.super_user)
        self.assertIsNotNone(ns.id)

    def test_user_add_other_user_to_namespace(self):
        ns = _create_namespace(self.super_user)
        # super
        s = AddUserToNameSpaceService(user=self.super_user)
        new_user_email1 = "montionugera+new1@gmail.com"
        nsmb = s.do_service(user_email=new_user_email1, role_key=NameSpaceMember.ROLE_MANAGER, namespace=ns)
        self.assertTrue(NameSpaceMember.ROLE_MANAGER in nsmb.get_roles())
        # normal
        s = AddUserToNameSpaceService(user=nsmb.member)
        new_user_email1 = "montionugera+new2@gmail.com"
        nsmb = s.do_service(user_email=new_user_email1, role_key=NameSpaceMember.ROLE_BOARD, namespace=ns)
        self.assertTrue(NameSpaceMember.ROLE_BOARD in nsmb.get_roles())
