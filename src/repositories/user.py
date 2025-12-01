from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import UserModel
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.schemas.user import UserCreateSchema
from datetime import datetime


class BaseUserRepository(ABC):

    @abstractmethod
    async def add(self, user: UserCreateSchema, hashed_password: str) -> UserModel: ...

    @abstractmethod
    async def get_by_id(self, id: int) -> UserModel | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserModel | None: ...

    @abstractmethod
    async def email_exists(self, email: str) -> bool: ...

    @abstractmethod
    async def save(self, user: UserModel) -> UserModel: ...

    @abstractmethod
    async def delete(self, user: UserModel) -> None: ...


@dataclass
class SQLAlchemyUserRepository:
    _session: AsyncSession

    async def add(self, user: UserCreateSchema, hashed_password: str) -> UserModel:
        user_model: UserModel = UserModel(
            **user.model_dump(exclude="password"), hashed_password=hashed_password
        )
        self._session.add(user_model)
        await self._session.flush()
        await self._session.refresh(user_model)
        await self._session.commit()
        return user_model

    async def get_by_id(self, id: int) -> UserModel | None:
        stmt = select(UserModel).where(
            UserModel.id == id, UserModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model

    async def get_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(
            UserModel.email == email, UserModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model

    async def email_exists(self, email: str) -> bool:
        stmt = select(UserModel.id).where(
            UserModel.email == email, UserModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def save(self, user: UserModel) -> UserModel:
        await self._session.commit()
        await self._session.refresh(user)

        return user

    async def delete(self, user: UserModel) -> None:
        user.is_deleted = True
        await self.save(user)


@dataclass
class InMemoryUserRepository(BaseUserRepository):
    users: list[UserModel] = None
    _id_counter: int = 1

    def __post_init__(self):
        if self.users is None:
            self.users = []

    async def add(self, user: UserCreateSchema, hashed_password: str) -> UserModel:
        now = datetime.now()
        new_user = UserModel(
            id=self._id_counter,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role,
            created_at=now,
            updated_at=now,
        )
        self._id_counter += 1
        self.users.append(new_user)
        return new_user

    async def get_by_id(self, id: int) -> UserModel | None:
        for u in self.users:
            if u.id == id and not getattr(u, "is_deleted", False):
                return u
        return None

    async def get_by_email(self, email: str) -> UserModel | None:
        for u in self.users:
            if u.email == email and not getattr(u, "is_deleted", False):
                return u
        return None

    async def email_exists(self, email: str) -> bool:
        return any(
            u.email == email and not getattr(u, "is_deleted", False) for u in self.users
        )

    async def save(self, user: UserModel) -> UserModel:
        return user

    async def delete(self, user: UserModel) -> None:
        user.is_deleted = True
