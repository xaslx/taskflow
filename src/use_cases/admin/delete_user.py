from dataclasses import dataclass
from src.repositories.user import BaseUserRepository
from src.models.user import UserModel
from src.exceptions.user import UserNotFoundException


@dataclass
class DeleteUserByAdminUseCase:
    _user_repository: BaseUserRepository


    async def execute(self, user_id: int) -> bool:

        user: UserModel | None = await self._user_repository.get_by_id(id=user_id)

        if not user:
            raise UserNotFoundException()

        await self._user_repository.delete(user=user)
        return True