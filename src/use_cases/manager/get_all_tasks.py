from dataclasses import dataclass
from src.repositories.task import BaseTaskRepository
from src.models.task import TaskModel
from src.schemas.task import TaskOut


@dataclass
class GetAllTasksUseCase:
    _task_repository: BaseTaskRepository

    async def execute(self, team_id: int) -> list[TaskOut]:

        tasks: list[TaskModel] = await self._task_repository.get_all_by_team_id(
            team_id=team_id
        )

        return [TaskOut.model_validate(task) for task in tasks]
