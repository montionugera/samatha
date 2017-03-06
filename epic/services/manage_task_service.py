from epic.models import Task
from samatha.exceptions import BusinessError
from samatha.services import UserActivityService
from samatha.validator import InputValidator


class CreateTaskService(UserActivityService):
    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return

    def _do_service(self, story=None, task_key=None, task_name=None, task_desc=None, task_estimate_hr=None,
                    task_sprint_no=None,responder=None,epic =None):
        self.input_validator.validate_require_parameter(story=story.key, task_key=task_key, task_name=task_name)
        self.input_validator.validate_not_too_long_parameter(task_key=task_key, task_name=task_name)
        self.input_validator.validate_shuoud_be_float_parameter(task_estimate_hr=task_estimate_hr)
        self.input_validator.validate_shuoud_be_int_parameter(task_sprint_no=task_sprint_no, allow_null=True)
        if Task.objects.filter(key=task_key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='story_key',
                reason_desc="This key already exist ")
        task = Task(key=task_key, name=task_name, desc=task_desc, estimate_hr=task_estimate_hr,
                    creator=self.user,responder=responder)
        task.story = story
        task.epic = epic
        task.save()

        return task


class UpdateTaskInfoService(UserActivityService):
    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return

    def _do_service(self, story=None, task_key=None, task_name=None, task_desc=None, task_estimate_hr=None,
                    task_sprint_no=None,responder=None):
        self.input_validator.validate_require_parameter(story=story.key, task_key=task_key, task_name=task_name)
        self.input_validator.validate_not_too_long_parameter(task_key=task_key, story_name=task_name)
        self.input_validator.validate_shuoud_be_float_parameter(task_estimate_hr=task_estimate_hr)
        self.input_validator.validate_shuoud_be_int_parameter(task_sprint_no=task_sprint_no, allow_null=True)
        if not Task.objects.filter(key=task_key).exists():
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='task_key',
                reason_desc="This key not exist ")

        task = Task.objects.get(key=task_key)
        task.name = task_name
        task.desc = task_desc
        task.story = story
        task.estimate_hr = task_estimate_hr
        task.sprint_no = task_sprint_no
        task.responder = responder
        task.save()
        return task


class UpdateTaskStateService(UserActivityService):
    def _check_can_do(self, **kwargs):
        if self.user.is_superuser:
            return
        task = kwargs.get('task',None)
        task_state = kwargs.get('task_state')
        available_states = task.get_updatable_states_for(self.user)
        if task_state not in available_states:
            raise BusinessError.get_invalid_parameter_exception(
                parameter_name='task_state',
                reason_desc="state %s not in updatable states (%s) "%(task_state,available_states))



    def _do_service(self, task=None, task_state=Task.STATE_PREPARE):
        self.input_validator.validate_require_parameter(task_state=task_state, task=task)
        task.task_state = task_state
        task.save()

        return task
