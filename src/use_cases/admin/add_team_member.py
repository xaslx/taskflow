from dataclasses import dataclass
from src.models.team import TeamModel
from src.exceptions.user import UserNotFoundException, AlreadyInTeamException
from src.exceptions.team import TeamNotFoundException
from src.models.user import UserModel
from src.repositories.team import BaseTeamRepository
from src.repositories.user import BaseUserRepository
from src.schemas.user import UserOut



@dataclass
class AddTeamMemberUseCase:
    _user_repository: BaseUserRepository
    _team_repository: BaseTeamRepository

    async def execute(self, user_id: int, team_id: int) -> UserOut:

        user: UserModel | None = await self._user_repository.get_by_id(id=user_id)

        if not user:
            raise UserNotFoundException()
        
        if user.team_id:
            raise AlreadyInTeamException()
        
        team: TeamModel | None = await self._team_repository.get_by_id(id=team_id)

        if not team:
            raise TeamNotFoundException()
        
        user.team_id = team.id
        await self._user_repository.save(user=user)

        return UserOut.model_validate(user)