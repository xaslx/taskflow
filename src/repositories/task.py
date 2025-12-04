from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.models.task import TaskModel, TaskCommentModel
from src.schemas.task import TaskCreate, TaskCommentCreate
import logging
import calendar
from datetime import date, datetime

logger = logging.getLogger(__name__)


class BaseTaskRepository(ABC):

    @abstractmethod
    async def add(self, task_data: TaskCreate, author_id: int) -> TaskModel: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> TaskModel | None: ...

    @abstractmethod
    async def get_all_by_team_id(self, team_id: int) -> list[TaskModel]: ...

    @abstractmethod
    async def save(self, task: TaskModel) -> TaskModel: ...

    @abstractmethod
    async def delete(self, task: TaskModel) -> None: ...

    @abstractmethod
    async def get_user_tasks_for_date(self, user_id: int, date: date) -> list[TaskModel]: ...

    async def get_user_tasks_for_month(
        self, 
        user_id: int, 
        year: int, 
        month: int
    ) -> list[TaskModel]: ...


@dataclass
class SQLAlchemyTaskRepository:
    _session: AsyncSession

    async def add(self, task_data: TaskCreate, author_id: int) -> TaskModel:
        try:
            task_model = TaskModel(**task_data.model_dump(), author_id=author_id)
            self._session.add(task_model)
            await self._session.flush()
            await self._session.refresh(task_model)
            await self._session.commit()
            return task_model
        except Exception as exc:
            logger.exception(f"Не удалось добавить данные: {task_data.model_dump()}")
            raise

    async def get_by_id(self, id: int) -> TaskModel | None:
        stmt = (
            select(TaskModel)
            .options(
                selectinload(TaskModel.author),
                selectinload(TaskModel.assignee),
                selectinload(TaskModel.team),
                selectinload(TaskModel.comments),
            )
            .where(TaskModel.id == id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_by_team_id(self, team_id: int) -> list[TaskModel]:
        stmt = (
            select(TaskModel)
            .options(
                selectinload(TaskModel.author),
                selectinload(TaskModel.assignee),
            )
            .where(TaskModel.team_id == team_id)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def save(self, task: TaskModel) -> TaskModel:
        try:
            await self._session.commit()
            await self._session.refresh(task)
            return task
        except Exception as exc:
            logger.exception(f"Не удалось сохранить данные: Task: {task.id}: {task.title}")
            raise

    async def delete(self, task: TaskModel) -> None:
        try:
            await self._session.delete(task)
            await self._session.commit()
        except Exception as exc:
            logger.exception(f"Не удалось удалить данные: Task: {task.id}: {task.title})")
            raise


    async def get_user_tasks_for_date(self, user_id: int, date: date) -> list[TaskModel]:

        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        
        stmt = (
            select(TaskModel)
            .options(
                selectinload(TaskModel.author),
                selectinload(TaskModel.assignee),
                selectinload(TaskModel.team),
                selectinload(TaskModel.comments),
            )
            .where(
                TaskModel.assignee_id == user_id,
                TaskModel.updated_at.between(start, end)
            )
            .order_by(TaskModel.updated_at.desc())
        )
        
        return (await self._session.execute(stmt)).scalars().all()
    

    async def get_user_tasks_for_month(
        self, 
        user_id: int, 
        year: int, 
        month: int
    ) -> list[TaskModel]:

        first_day = date(year, month, 1)
        

        _, last_day_num = calendar.monthrange(year, month)
        last_day = date(year, month, last_day_num)
        

        start_datetime = datetime.combine(first_day, datetime.min.time())
        end_datetime = datetime.combine(last_day, datetime.max.time())
        
        stmt = (
            select(TaskModel)
            .options(
                selectinload(TaskModel.author),
                selectinload(TaskModel.assignee),
                selectinload(TaskModel.team),
                selectinload(TaskModel.comments),
            )
            .where(
                TaskModel.assignee_id == user_id,
                TaskModel.updated_at >= start_datetime,
                TaskModel.updated_at <= end_datetime
            )
            .order_by(TaskModel.updated_at.desc())
        )
        
        result = await self._session.execute(stmt)
        return result.scalars().all()


class BaseTaskCommentRepository(ABC):
    @abstractmethod
    async def add(
        self, comment_data: TaskCommentCreate, author_id: int, task_id: int
    ) -> TaskCommentModel: ...


@dataclass
class SQLAlchemyTaskCommentRepository:
    _session: AsyncSession

    async def add(
        self, comment_data: TaskCommentCreate, author_id: int, task_id: int
    ) -> TaskCommentModel:
        try:
            comment_model = TaskCommentModel(
                **comment_data.model_dump(), author_id=author_id, task_id=task_id
            )
            self._session.add(comment_model)
            await self._session.flush()
            await self._session.refresh(comment_model)
            await self._session.commit()
            return comment_model
        except Exception as exc:
            logger.exception(f"Не удалось добавить данные: {comment_data.model_dump()}")
            raise