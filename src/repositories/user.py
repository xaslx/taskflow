from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import UserModel
from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.schemas.user import UserCreateSchema


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
        user_model: UserModel = UserModel(**user.model_dump(exclude='password'), hashed_password=hashed_password)
        self._session.add(user_model)
        await self._session.flush()
        await self._session.refresh(user_model)
        await self._session.commit()
        return user_model
    
    
    async def get_by_id(self, id: int) -> UserModel | None:
        stmt = select(UserModel).where(
            UserModel.id == id,
            UserModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model
    
    async def get_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(
            UserModel.email == email,
            UserModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model
    
    
    async def email_exists(self, email: str) -> bool:
        stmt = select(UserModel.id).where(
            UserModel.email == email,
            UserModel.is_deleted == False
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