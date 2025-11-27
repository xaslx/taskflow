from abc import ABC
from dataclasses import dataclass
from src.repositories.team import BaseTeamRepository
from src.repositories.user import BaseUserRepository
from src.schemas.user import UserOut
from src.models.team import TeamModel
from src.models.user import UserModel
from src.exceptions.user import UserNotFoundException, AlreadyInTeamException, UserNotInTeamException
from src.exceptions.team import TeamNotFoundException


@dataclass
class BaseTeamMemberUseCase(ABC):
    _user_repository: BaseUserRepository
    _team_repository: BaseTeamRepository

    async def _validate_and_get_model(self, user_id: int, team_id: int) -> tuple[UserModel, TeamModel]:

        user: UserModel | None = await self._user_repository.get_by_id(id=user_id)

        if not user:
            raise UserNotFoundException()
        
        team: TeamModel | None = await self._team_repository.get_by_id(id=team_id)

        if not team:
            raise TeamNotFoundException()
        
        return user, team
    



@dataclass
class AddTeamMemberUseCase(BaseTeamMemberUseCase):

    async def execute(self, user_id: int, team_id: int) -> UserOut:

        user, team = await self._validate_and_get_model(user_id, team_id)
        
        if user.team_id:
            raise AlreadyInTeamException()
        
        user.team_id = team.id
        user: UserModel = await self._user_repository.save(user=user)

        return UserOut.model_validate(user)



@dataclass  
class DeleteTeamMemberUseCase(BaseTeamMemberUseCase):

    async def execute(self, user_id: int, team_id: int) -> UserOut:

        user, team = await self._validate_and_get_model(user_id, team_id)
        
        if user.team_id != team.id:
            raise UserNotInTeamException()
        
        user.team_id = None
        user: UserModel = await self._user_repository.save(user=user)
        return UserOut.model_validate(user)