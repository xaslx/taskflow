from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.models.evaluation import EvaluationModel
from src.schemas.evaluation import EvaluationCreate
import logging


logger = logging.getLogger(__name__)


class BaseEvaluationRepository(ABC):

    @abstractmethod
    async def add(
        self, evaluation_data: EvaluationCreate, evaluator_id: int, user_id: int
    ) -> EvaluationModel: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[EvaluationModel]: ...

    @abstractmethod
    async def get_by_task_id(self, task_id: int) -> EvaluationModel | None: ...


@dataclass
class SQLAlchemyEvaluationRepository:
    _session: AsyncSession

    async def add(
        self, evaluation_data: EvaluationCreate, evaluator_id: int, user_id: int
    ) -> EvaluationModel:
        
        try:
            evaluation_model = EvaluationModel(
                **evaluation_data.model_dump(), evaluator_id=evaluator_id, user_id=user_id
            )
            self._session.add(evaluation_model)
            await self._session.flush()
            await self._session.refresh(evaluation_model)
            await self._session.commit()
            return evaluation_model
        except Exception as exc:
            logger.exception(f"Не удалось добавить данные: {evaluation_data.model_dump()}")
            raise

    async def get_by_user_id(self, user_id: int) -> list[EvaluationModel]:
        stmt = (
            select(EvaluationModel)
            .options(
                selectinload(EvaluationModel.task),
                selectinload(EvaluationModel.evaluator),
            )
            .where(EvaluationModel.user_id == user_id)
            .order_by(EvaluationModel.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_task_id(self, task_id: int) -> EvaluationModel | None:
        stmt = select(EvaluationModel).where(EvaluationModel.task_id == task_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
