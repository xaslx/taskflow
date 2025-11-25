from dataclasses import dataclass
from src.schemas.team import CreateTeamSchema, TeamOut
from src.repositories.team import BaseTeamRepository
from src.models.team import TeamModel
from src.schemas.user import UserOut
from uuid import uuid4


@dataclass
class CreateTeamUseCase:
    _team_repository: BaseTeamRepository


    async def execute(self, team: CreateTeamSchema) -> TeamOut:

        code: str = str(uuid4())
        team: TeamModel = await self._team_repository.add(team=team, code=code)
        return TeamOut(
            id=team.id,
            name=team.name,
            code=team.code,
            users=[],
        )