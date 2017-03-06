from epic.models import Story
from samatha.exceptions import BusinessError
from samatha.services import UserActivityService
from samatha.validator import InputValidator


class CreateStoryService(UserActivityService):
    input_validator = InputValidator()

    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return

    def _do_service(self, epic=None, story_key=None, story_name=None, story_desc=None):
        self.input_validator.validate_require_parameter(epic=epic.key, story_key=story_key, story_name=story_name)
        self.input_validator.validate_not_too_long_parameter(story_key=story_key, story_name=story_name)
        if Story.objects.filter(key=story_key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='story_key',
                reason_desc="This key already exist ")
        story = Story(key=story_key, name=story_name, desc=story_desc,
                    creator=self.user)
        story.epic = epic
        story.save()

        return story


class UpdateStoryService(UserActivityService):
    input_validator = InputValidator()

    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return

    def _do_service(self, epic=None, story_key=None, story_name=None, story_desc=None):
        self.input_validator.validate_require_parameter(epic=epic.key, story_key=story_key, story_name=story_name)
        self.input_validator.validate_not_too_long_parameter(story_key=story_key, story_name=story_name)
        if not Story.objects.filter(key=story_key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='story_key',
                reason_desc="This key not exist ")

        story = Story.objects.get(key=story_key)
        story.name = story_name
        story.desc = story_desc
        story.epic = epic
        story.save()
        return story


class UpdateStoryStatusService(UserActivityService):
    input_validator = InputValidator()

    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return
        story = kwargs.get('story')