from epic.models import Task
from samatha.services import UserActivityService
from sprint.models import SprintSlot, SprintTask

# Manange task


class AddTaskToSprintService(UserActivityService):
    def _do_service(self, sprint_slot=None, task=None):
        self.input_validator.validate_require_parameter(sprint_slot=sprint_slot, task=task)

        if not SprintTask.objects.filter(sprint_slot=sprint_slot, task=task).exists():
            st = SprintTask(sprint_slot=sprint_slot, task=task)
            st.save()
        else:
            st = SprintTask.objects.get(sprint_slot=sprint_slot, task=task)

        return st


class RemoveTaskFromSprintService(UserActivityService):
    def _do_service(self, sprint_slot=None, task=None):
        self.input_validator.validate_require_parameter(sprint_slot=sprint_slot, task=task)
        SprintTask.objects.filter(sprint_slot=sprint_slot, task=task).delete()
        return sprint_slot


class AddAllTaskOfStoryToSprintService(UserActivityService):
    def _do_service(self, sprint_slot=None, story=None):
        self.input_validator.validate_require_parameter(sprint_slot=sprint_slot, story=story)
        tasks = list(Task.objects.filter(story=story))
        for task in tasks:
            _s = AddTaskToSprintService(self.user)
            _s.do_service(sprint_slot=sprint_slot, task=task)

        return tasks


# Manange Sprint State

class CreateSprintService(UserActivityService):
    def _do_service(self, sprint_no=None, name_space=None):
        self.input_validator.validate_require_parameter(name_space=name_space)
        sprint_slot = SprintSlot.get_or_create_sprint_slot(sprint_no=sprint_no, name_space=name_space)

        return sprint_slot


class CleanTaskInSprintService(UserActivityService):
    AUTO_MIGRATE_STRATEGY_MOVE_NEXT = 'MN'
    AUTO_MIGRATE_STRATEGY_CLEAR = 'CL'

    def _do_service(self, sprint_slot=None,
                    auto_migrate_strategy=AUTO_MIGRATE_STRATEGY_MOVE_NEXT):
        self.input_validator.validate_require_parameter(sprint_slot=sprint_slot,
                                                        auto_migrate_strategy=auto_migrate_strategy)

        if auto_migrate_strategy == CleanTaskInSprintService.AUTO_MIGRATE_STRATEGY_MOVE_NEXT:
            self._move_all_task_in_this_sprint_to_next_sprint(sprint_slot=sprint_slot)

        return sprint_slot

    def _move_all_task_in_this_sprint_to_next_sprint(self, sprint_slot=None):

        tasks = list(SprintTask.objects.filter(task__task_state__in=[
            Task.STATE_TODO,
            Task.STATE_INPROGRESS,
            Task.STATE_TOVERIFY,
            Task.STATE_VERIFYING,
            Task.STATE_TEST_F,
            Task.STATE_TEST_P,
        ]))
        next_sprint_no = sprint_slot.sprint_no + 1
        _cs = CreateSprintService(self.user)
        next_sprint_slot = _cs.do_service(sprint_no=next_sprint_no, name_space=sprint_slot.namespace)
        for task in tasks:
            _s = AddTaskToSprintService(self.user)
            _s.do_service(sprint_slot=next_sprint_slot, task=task)
