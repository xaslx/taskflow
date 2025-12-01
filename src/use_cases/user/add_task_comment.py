from dataclasses import dataclass
from src.models.task import TaskCommentModel, TaskModel
from src.exceptions.task import TaskNotFoundException
from src.repositories.task import BaseTaskCommentRepository, BaseTaskRepository
from src.schemas.task import TaskCommentCreate, TaskCommentOut
from src.exceptions.user import ForbiddenException


@dataclass
class CreateCommentUseCase:
    _task_comment_repository: BaseTaskCommentRepository
    _task_repository: BaseTaskRepository

    async def execute(
        self, task_id: int, comment: TaskCommentCreate, author_id: int, team_id: int
    ) -> TaskCommentOut:

        task: TaskModel | None = await self._task_repository.get_by_id(id=task_id)

        if not task:
            raise TaskNotFoundException()

        if task.team_id != team_id:
            raise ForbiddenException()

        new_comment: TaskCommentModel = await self._task_comment_repository.add(
            comment_data=comment, author_id=author_id, task_id=task_id
        )
        return TaskCommentOut.model_validate(new_comment)
