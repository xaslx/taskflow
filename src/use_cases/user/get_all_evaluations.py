from dataclasses import dataclass
from src.schemas.evaluation import EvaluationOut
from src.repositories.evaluation import BaseEvaluationRepository
from src.models.evaluation import EvaluationModel



@dataclass
class GetAllEvaluationsUseCase:
    _evaluation_repository: BaseEvaluationRepository

    async def execute(self, user_id: int) -> list[EvaluationOut]:

        evaluations: list[EvaluationModel] = await self._evaluation_repository.get_by_user_id(user_id=user_id)

        return [EvaluationOut.model_validate(ev) for ev in evaluations]