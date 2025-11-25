from collections.abc import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.config import Config
from src.database.postgres import new_session_maker
from src.use_cases.user.register import RegisterUserUseCase
from src.repositories.user import BaseUserRepository, SQLAlchemyUserRepository
from src.services.hash import BaseHashService, BCryptHashService
from src.services.jwt import JWTService, JWTServiceImpl



class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


    #services
    @provide(scope=Scope.REQUEST)
    def get_hash_service(self) -> BaseHashService:
        return BCryptHashService()
    
    @provide(scope=Scope.REQUEST)
    def get_jwt_service(self, config: Config) -> JWTService:
        return JWTServiceImpl(config=config)


    #repositories
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(_session=session)


    #use cases
    @provide(scope=Scope.REQUEST)
    def get_register_user_use_case(self, user_repository: BaseUserRepository, hash_service: BaseHashService) -> RegisterUserUseCase:
        return RegisterUserUseCase(_user_repository=user_repository, _hash_service=hash_service)