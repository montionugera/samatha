from namespace.models import NameSpace
from samatha.services import UserActivityService


class ActivityModel(object):
    action = 'CH_STATUS'
    sth = 'STORY'


class NameSpaceService(UserActivityService):
    object_type = 'NAMESPACE'
    def _check_can_do(self,*kwargs):
        return self.user.is_superuser


S_ACTIONS = ['CREATE_NS']


class EpicService(object):
    def get_possible_activities(self):
        pass


# #user can do #(kind of thing) on the #thing in #s.epic
# user can edit ?

class StoryActivityManager(object):
    def get_possible_activities(self):
        pass
