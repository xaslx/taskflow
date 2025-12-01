from dataclasses import dataclass
from src.schemas.user import UserCreateSchema, UserOut
from src.repositories.user import BaseUserRepository
from src.models.user import UserModel
from src.exceptions.user import UserAlreadyExists
from src.services.hash import BaseHashService


@dataclass
class RegisterUserUseCase:
    _user_repository: BaseUserRepository
    _hash_service: BaseHashService

    async def execute(self, new_user: UserCreateSchema) -> UserOut:

        user: UserModel | None = await self._user_repository.get_by_email(
            email=new_user.email
        )

        if user:
            raise UserAlreadyExists()

        hashed_password: str = self._hash_service.get_password_hash(
            password=new_user.password
        )

        user: UserModel = await self._user_repository.add(
            user=new_user, hashed_password=hashed_password
        )
        return UserOut.model_validate(user)
