from dataclasses import dataclass
from src.models.task import TaskModel
from src.schemas.task import TaskUpdate, TaskOut
from src.repositories.task import BaseTaskRepository
from src.exceptions.task import TaskNotFoundException
from src.exceptions.user import ForbiddenException


@dataclass
class UpdateTaskUseCase:
    _task_repository: BaseTaskRepository

    async def execute(
        self, updated_task: TaskUpdate, task_id: int, team_id: int, author_id: int
    ) -> TaskOut:

        task: TaskModel | None = await self._task_repository.get_by_id(id=task_id)

        if not task:
            raise TaskNotFoundException()

        if task.author_id != author_id:
            raise ForbiddenException()

        if task.team_id != team_id:
            raise ForbiddenException()

        if updated_task.title:
            task.title = updated_task.title

        if updated_task.assignee_id:
            task.assignee_id = updated_task.assignee_id

        if updated_task.deadline:
            task.deadline = updated_task.deadline

        if updated_task.description:
            task.description = updated_task.description

        if updated_task.status:
            task.status = updated_task.status

        task = await self._task_repository.save(task=task)
        return TaskOut.model_validate(task)
