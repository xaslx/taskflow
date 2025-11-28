from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.models.task import TaskModel, TaskCommentModel
from src.schemas.task import TaskCreate, TaskCommentCreate



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


@dataclass
class SQLAlchemyTaskRepository:
    _session: AsyncSession

    async def add(self, task_data: TaskCreate, author_id: int) -> TaskModel:
        task_model = TaskModel(
            **task_data.model_dump(),
            author_id=author_id
        )
        self._session.add(task_model)
        await self._session.flush()
        await self._session.refresh(task_model)
        await self._session.commit()
        return task_model
    

    async def get_by_id(self, id: int) -> TaskModel | None:
        stmt = (
            select(TaskModel)
            .options(
                selectinload(TaskModel.author),
                selectinload(TaskModel.assignee),
                selectinload(TaskModel.team),
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
        await self._session.commit()
        await self._session.refresh(task)
        return task
    

    async def delete(self, task: TaskModel) -> None:
        await self._session.delete(task)
        await self._session.commit()





class BaseTaskCommentRepository(ABC):
    @abstractmethod
    async def add(self, comment_data: TaskCommentCreate, author_id: int, task_id: int) -> TaskCommentModel: ...


@dataclass
class SQLAlchemyTaskCommentRepository:
    _session: AsyncSession

    async def add(self, comment_data: TaskCommentCreate, author_id: int, task_id: int) -> TaskCommentModel:
        comment_model = TaskCommentModel(
            **comment_data.model_dump(),
            author_id=author_id,
            task_id=task_id
        )
        self._session.add(comment_model)
        await self._session.flush()
        await self._session.refresh(comment_model)
        await self._session.commit()
        return comment_model