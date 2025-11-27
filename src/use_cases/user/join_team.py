from dataclasses import dataclass
from src.exceptions.user import AlreadyInTeamException
from src.exceptions.team import TeamNotFoundException
from src.models.user import UserModel
from src.repositories.team import BaseTeamRepository
from src.models.team import TeamModel
from src.repositories.user import BaseUserRepository
from src.schemas.user import UserOut


@dataclass
class JoinTeamByCodeUseCase:
    _team_repository: BaseTeamRepository
    _user_repository: BaseUserRepository

    async def execute(self, user: UserModel, code: str) -> UserOut:


        team: TeamModel | None = await self._team_repository.get_by_code(code=code)

        if not team:
            raise TeamNotFoundException()
        
        if user.team_id:
            raise AlreadyInTeamException()

        user.team_id = team.id
        user: UserModel = await self._user_repository.save(user=user)
        return UserOut.model_validate(user)