from dataclasses import dataclass
from src.schemas.team import TeamOutWithUsers
from src.models.team import TeamModel
from src.repositories.team import BaseTeamRepository



@dataclass
class GetTeamInfoUseCase:
    _team_repository: BaseTeamRepository

    async def execute(self, team_id: int) -> TeamOutWithUsers | None:

        team: TeamModel | None = await self._team_repository.get_by_id(id=team_id)

        if not team:
            return None
        return TeamOutWithUsers.model_validate(team)