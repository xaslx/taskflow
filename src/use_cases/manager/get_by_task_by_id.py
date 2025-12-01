from dataclasses import dataclass
from src.schemas.task import TaskOut
from src.models.task import TaskModel
from src.repositories.task import BaseTaskRepository


@dataclass
class GetTaskByIdUseCase:
    _task_repository: BaseTaskRepository

    async def execute(self, task_id: int, team_id: int) -> TaskOut | None:

        task: TaskModel | None = await self._task_repository.get_by_id(id=task_id)

        if not task or task.team_id != team_id:
            return None
        return TaskOut.model_validate(task)
