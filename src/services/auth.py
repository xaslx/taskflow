from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.repositories.user import BaseUserRepository
from src.services.hash import BaseHashService
from src.services.jwt import JWTService
from src.models.user import UserModel
from src.exceptions.user import IncorrectEmailOrPasswordException, UserNotFoundException


@dataclass
class BaseAuthService(ABC):

    _user_repository: BaseUserRepository
    _hash_service: BaseHashService
    _jwt_service: JWTService

    @abstractmethod
    async def authenticate_user(self, username: str, password: str): ...

    @abstractmethod
    async def get_current_user(self, token: str): ...


@dataclass
class AuthServiceImpl(BaseAuthService):

    async def authenticate_user(self, email: str, password: str) -> UserModel | None:
        user: UserModel | None = await self._user_repository.get_by_email(email=email)

        if user is None:
            raise IncorrectEmailOrPasswordException()

        if not self._hash_service.verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            raise IncorrectEmailOrPasswordException()

        return user

    async def get_current_user(self, token: str) -> UserModel | None:
        payload = self._jwt_service.verify_access_token(token=token)

        if not payload:
            return None

        user_id = payload.get("sub")
        user: UserModel | None = await self._user_repository.get_by_id(id=int(user_id))

        if user is None:
            raise UserNotFoundException()

        return user
