from dataclasses import dataclass
from src.models.task import TaskModel
from src.models.team import TeamModel
from src.models.user import UserModel
from src.repositories.task import BaseTaskRepository
from src.repositories.team import BaseTeamRepository
from src.repositories.user import BaseUserRepository
from src.schemas.task import TaskCreate, TaskOut
from src.exceptions.team import TeamNotFoundException
from src.exceptions.user import UserNotFoundException, UserNotInTeamException


@dataclass
class CreateTaskUseCase:
    _task_repository: BaseTaskRepository
    _team_repository: BaseTeamRepository
    _user_repository: BaseUserRepository

    async def execute(self, task: TaskCreate, author_id: int) -> TaskOut:

        team: TeamModel | None = await self._team_repository.get_by_id(task.team_id)

        if not team:
            raise TeamNotFoundException()

        author: UserModel | None = await self._user_repository.get_by_id(author_id)

        if not author:
            raise UserNotFoundException()

        if author.team_id != team.id:
            raise UserNotInTeamException()

        task_model: TaskModel = await self._task_repository.add(task, author_id)
        full_task_model = await self._task_repository.get_by_id(task_model.id)
        return TaskOut.model_validate(full_task_model)
