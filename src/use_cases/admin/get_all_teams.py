from dataclasses import dataclass
from src.repositories.team import BaseTeamRepository
from src.schemas.pagination import PaginatedResponse, PaginationParams
from src.schemas.team import TeamOut



@dataclass
class GetAllTeamsUseCase:
    _team_repository: BaseTeamRepository

    async def execute(self, pagination: PaginationParams) -> PaginatedResponse[TeamOut]:

        paginated_result: PaginatedResponse[TeamOut] = await self._team_repository.get_paginated(pagination=pagination)
        return paginated_result