from dataclasses import dataclass
from src.repositories.team import BaseTeamRepository
from src.schemas.team import TeamOut
from src.models.team import TeamModel



@dataclass
class GetAllTeamsUseCase:
    _team_repository: BaseTeamRepository

    async def execute(self) -> list[TeamOut]:

        teams: list[TeamModel] = await self._team_repository.get_all()

        return [TeamOut.model_validate(team) for team in teams]