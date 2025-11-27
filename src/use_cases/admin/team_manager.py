from abc import ABC
from dataclasses import dataclass
from src.repositories.team import BaseTeamRepository
from src.repositories.user import BaseUserRepository
from src.schemas.user import UserOut
from src.models.team import TeamModel
from src.models.user import UserModel
from src.exceptions.user import UserNotFoundException, AlreadyInTeamException, UserNotInTeamException, InvalidRoleException
from src.exceptions.team import TeamNotFoundException
from src.schemas.user import UserRole



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

    async def _save_and_return_user(self, user: UserModel) -> UserOut:

        updated_user: UserModel = await self._user_repository.save(user=user)
        return UserOut.model_validate(updated_user)
    



@dataclass
class AddTeamMemberUseCase(BaseTeamMemberUseCase):

    async def execute(self, user_id: int, team_id: int) -> UserOut:

        user, team = await self._validate_and_get_model(user_id, team_id)
        
        if user.team_id:
            raise AlreadyInTeamException()
        
        user.team_id = team.id
        return await self._save_and_return_user(user)



@dataclass  
class DeleteTeamMemberUseCase(BaseTeamMemberUseCase):

    async def execute(self, user_id: int, team_id: int) -> UserOut:

        user, team = await self._validate_and_get_model(user_id, team_id)
        
        if user.team_id != team.id:
            raise UserNotInTeamException()
        
        user.team_id = None
        return await self._save_and_return_user(user)

@dataclass
class ChangeUserRoleUseCase(BaseTeamMemberUseCase):

    async def execute(self, user_id: int, team_id: int, new_role: UserRole) -> UserOut:

        user, team = await self._validate_and_get_model(user_id, team_id)

        if user.team_id != team.id:
            raise UserNotInTeamException()
        
        if new_role not in [UserRole.USER, UserRole.MANAGER]:
            raise InvalidRoleException()
        
        user.role = new_role
        return await self._save_and_return_user(user)