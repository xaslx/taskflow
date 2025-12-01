from dataclasses import dataclass
from src.models.user import UserModel
from src.repositories.user import BaseUserRepository
from src.exceptions.user import UserNotFoundException


@dataclass
class DeleteUserUseCase:
    _user_repository: BaseUserRepository

    async def execute(self, user: UserModel) -> bool:

        await self._user_repository.delete(user=user)
        return True
