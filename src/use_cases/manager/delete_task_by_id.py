from dataclasses import dataclass
from src.models.task import TaskModel
from src.repositories.task import BaseTaskRepository
from src.exceptions.task import TaskNotFoundException
from src.exceptions.user import ForbiddenException


@dataclass
class DeleteTaskByIdUseCase:
    _task_repository: BaseTaskRepository

    async def execute(self, task_id: int, user_id: int, user_team_id: int) -> None:

        task: TaskModel | None = await self._task_repository.get_by_id(id=task_id)

        if not task:
            raise TaskNotFoundException()

        if task.team_id != user_team_id:
            raise ForbiddenException()

        if task.author_id != user_id:
            raise ForbiddenException()

        await self._task_repository.delete(task=task)
