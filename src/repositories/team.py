from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.schemas.team import TeamOut
from src.schemas.pagination import PaginatedResponse, PaginationParams
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
    async def get_paginated(
        self, pagination: PaginationParams
    ) -> PaginatedResponse[TeamOut]: ...

    @abstractmethod
    async def save(self, team: TeamModel) -> TeamModel: ...


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

    async def get_paginated(
        self, pagination: PaginationParams
    ) -> PaginatedResponse[TeamOut]:
        count_stmt = select(func.count(TeamModel.id))
        total_result = await self._session.execute(count_stmt)
        total = total_result.scalar()

        data_stmt = (
            select(TeamModel)
            .options(selectinload(TeamModel.users))
            .offset(pagination.offset)
            .limit(pagination.size)
        )
        result = await self._session.execute(data_stmt)
        items = result.scalars().all()

        items_out = [TeamOut.model_validate(team) for team in items]

        pages = (total + pagination.size - 1) // pagination.size

        return PaginatedResponse(
            items=items_out,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages,
        )

    async def save(self, team: TeamModel) -> TeamModel:
        await self._session.commit()
        await self._session.refresh(team)
        return team
