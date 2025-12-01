from dataclasses import dataclass
from src.models.evaluation import EvaluationModel
from src.schemas.evaluation import EvaluationCreate, EvaluationOut
from src.repositories.evaluation import BaseEvaluationRepository
from src.repositories.task import BaseTaskRepository
from src.exceptions.task import TaskNotFoundException
from src.exceptions.user import ForbiddenException
from src.exceptions.task import TaskNotAssigneeException, TaskNotCompletedException
from src.models.task import TaskModel
from src.exceptions.evaluation import EvaluationAlreadyExistsException


@dataclass
class CreateEvaluationUseCase:
    _evaluation_repository: BaseEvaluationRepository
    _task_repository: BaseTaskRepository

    async def execute(
        self, evaluation: EvaluationCreate, evaluator_id: int, team_id: int
    ) -> EvaluationOut:

        task: TaskModel | None = await self._task_repository.get_by_id(
            id=evaluation.task_id
        )

        if not task:
            raise TaskNotFoundException()

        if task.team_id != team_id:
            raise ForbiddenException()

        if task.status != "completed":
            raise TaskNotCompletedException()

        if not task.assignee_id:
            raise TaskNotAssigneeException()

        existing_evaluation: EvaluationModel | None = (
            await self._evaluation_repository.get_by_task_id(task.id)
        )

        if existing_evaluation:
            raise EvaluationAlreadyExistsException()

        evaluation_model: EvaluationModel = await self._evaluation_repository.add(
            evaluation_data=evaluation,
            evaluator_id=evaluator_id,
            user_id=task.assignee_id,
        )

        return EvaluationOut.model_validate(evaluation_model)
