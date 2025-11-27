from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from abc import ABC, abstractmethod

from src.models.team import TeamModel
from src.schemas.team import CreateTeamSchema


class BaseTeamRepository(ABC):

    @abstractmethod
    async def add(self, team: CreateTeamSchema, code: str) -> TeamModel: ...
    
    @abstractmethod
    async def get_by_id(self, id: int) -> TeamModel | None: ...

    @abstractmethod
    async def get_by_code(self, code: str) -> TeamModel | None: ...
    
    @abstractmethod
    async def get_all(self) -> list[TeamModel]: ...
    
    @abstractmethod
    async def save(self, team: TeamModel) -> TeamModel: ...
    
    @abstractmethod
    async def delete(self, team: TeamModel) -> None: ...


@dataclass
class SQLAlchemyTeamRepository:
    _session: AsyncSession


    async def add(self, team: CreateTeamSchema, code: str) -> TeamModel:
        team_model = TeamModel(**team.model_dump(), code=code)
        self._session.add(team_model)
        await self._session.flush()
        await self._session.refresh(team_model)
        await self._session.commit()
        return team_model
    

    async def get_by_id(self, id: int) -> TeamModel | None:
        stmt = (
            select(TeamModel)
            .options(selectinload(TeamModel.users))
            .where(TeamModel.id == id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
        
    async def get_by_code(self, code: str) -> TeamModel | None:
        stmt = (
            select(TeamModel)
            .options(selectinload(TeamModel.users))
            .where(TeamModel.code == code)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[TeamModel]:
        stmt = (
            select(TeamModel)
            .options(selectinload(TeamModel.users))
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
    

    async def save(self, team: TeamModel) -> TeamModel:
        await self._session.commit()
        await self._session.refresh(team)
        
        return team
    

    async def delete(self, team: TeamModel) -> None:
        team.is_deleted = True
        await self.save(team)
