from pydantic import ValidationError
import pytest
from src.models.user import UserModel
from src.repositories.user import BaseUserRepository
from src.use_cases.user.register import RegisterUserUseCase
from src.exceptions.user import UserAlreadyExists, IncorrectEmailOrPasswordException
from src.schemas.user import (
    UserCreateSchema,
    UserLoginSchema,
    UserOut,
    UserUpdateSchema,
)
from src.use_cases.user.login import LoginUserUseCase
from src.use_cases.user.update_user import UpdateUserUseCase


@pytest.mark.asyncio
class TestRegisterUserUseCase:

    async def test_register_user_success(
        self, register_usecase: RegisterUserUseCase, user_repository: BaseUserRepository
    ):
        new_user = UserCreateSchema(email="test@test.com", password="test123456")
        result = await register_usecase.execute(new_user)
        assert result.email == "test@test.com"
        assert await user_repository.email_exists("test@test.com") is True

    @pytest.mark.parametrize(
        "invalid_password",
        [
            "12345",
            "abcdef",
            "ABCDEF",
            "123456",
            "абвгде123",
        ],
    )
    async def test_register_user_invalid_password(self, invalid_password):
        with pytest.raises(ValidationError):
            UserCreateSchema(email="test2@test.com", password=invalid_password)

    async def test_register_user_already_exists(
        self, register_usecase: RegisterUserUseCase
    ):
        new_user = UserCreateSchema(email="test@test.com", password="test123456")
        await register_usecase.execute(new_user)

        with pytest.raises(UserAlreadyExists):
            await register_usecase.execute(new_user)


@pytest.mark.asyncio
class TestLoginUserUseCase:

    async def test_login_user_success(self, login_use_case: LoginUserUseCase):
        credentials: UserLoginSchema = UserLoginSchema(
            email="testuser@gmail.com", password="testtest123"
        )
        tokens = await login_use_case.execute(credentials=credentials)
        assert tokens

    async def test_login_user_fail(self, login_use_case: LoginUserUseCase):
        with pytest.raises(IncorrectEmailOrPasswordException):
            credentials: UserLoginSchema = UserLoginSchema(
                email="testuser@gmail.com", password="testtest100"
            )
            await login_use_case.execute(credentials=credentials)


@pytest.mark.asyncio
class TestUpdateUserUseCase:

    async def test_update_email(
        self,
        update_user_use_case: UpdateUserUseCase,
        test_user: UserModel,
        user_repository: BaseUserRepository,
    ):
        old_email: str = test_user.email
        update_data: UserUpdateSchema = UserUpdateSchema(email="new_email@gmail.com")
        user_out: UserOut = await update_user_use_case.execute(
            updated_user=update_data, user=test_user
        )

        assert user_out.email != old_email

        updated_user_model: UserModel | None = await user_repository.get_by_email(
            email="new_email@gmail.com"
        )
        assert updated_user_model.id == test_user.id

    async def test_update_password(
        self,
        update_user_use_case: UpdateUserUseCase,
        test_user: UserModel,
        user_repository: BaseUserRepository,
    ):

        old_hashed: str = test_user.hashed_password
        new_password: str = "newpass123"
        update_data = UserUpdateSchema(password=new_password)

        await update_user_use_case.execute(updated_user=update_data, user=test_user)
        assert test_user.hashed_password != old_hashed
        updated_user_model: UserModel | None = await user_repository.get_by_email(
            email=test_user.email
        )
        assert updated_user_model.hashed_password == test_user.hashed_password
