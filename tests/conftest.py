from src.models.user import UserModel
from src.services.hash import BaseHashService, BCryptHashService
from src.repositories.user import InMemoryUserRepository, BaseUserRepository
import pytest
from src.use_cases.user.register import RegisterUserUseCase
from src.services.auth import BaseAuthService, AuthServiceImpl
from src.use_cases.user.update_user import UpdateUserUseCase
from src.use_cases.user.login import LoginUserUseCase
from src.services.jwt import JWTService, JWTServiceImpl
from src.config import Config
from src.schemas.user import UserCreateSchema
import pytest_asyncio


@pytest.fixture
def config() -> Config:
    return Config()


@pytest.fixture
def hash_service() -> BaseHashService:

    return BCryptHashService()


@pytest.fixture
def user_repository() -> BaseUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def register_usecase(
    user_repository: BaseUserRepository, hash_service: BaseHashService
) -> RegisterUserUseCase:
    return RegisterUserUseCase(
        _user_repository=user_repository, _hash_service=hash_service
    )


@pytest.fixture
def jwt_service(config: Config) -> JWTService:
    return JWTServiceImpl(config=config)


@pytest.fixture
def auth_service(
    user_repository: BaseUserRepository,
    hash_service: BaseHashService,
    jwt_service: JWTService,
) -> BaseAuthService:

    return AuthServiceImpl(
        _user_repository=user_repository,
        _hash_service=hash_service,
        _jwt_service=jwt_service,
    )


@pytest.fixture
def login_use_case(
    user_repository: BaseUserRepository,
    auth_service: BaseAuthService,
    jwt_service: JWTService,
) -> LoginUserUseCase:

    return LoginUserUseCase(
        _user_repository=user_repository,
        _auth_service=auth_service,
        _jwt_service=jwt_service,
    )


@pytest_asyncio.fixture(autouse=True)
async def test_user(
    user_repository: BaseUserRepository, hash_service: BaseHashService
) -> UserModel:
    user: UserCreateSchema = UserCreateSchema(
        email="testuser@gmail.com", password="testtest123"
    )
    hashed_password: str = hash_service.get_password_hash(password=user.password)
    user = await user_repository.add(user, hashed_password=hashed_password)
    return user


@pytest_asyncio.fixture
async def update_user_use_case(
    user_repository: BaseUserRepository,
    hash_service: BaseHashService,
) -> UpdateUserUseCase:

    return UpdateUserUseCase(
        _user_repository=user_repository,
        _hash_service=hash_service,
    )
