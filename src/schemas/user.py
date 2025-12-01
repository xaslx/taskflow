from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from enum import StrEnum
import re
from datetime import datetime


def validate_password(value: str) -> str:

    if len(value) < 6 or len(value) > 20:
        raise ValueError("Пароль должен быть от 6 до 20 символов")

    password_pattern = r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]*$'
    if not re.match(password_pattern, value):
        raise ValueError(
            "Пароль может содержать только латинские буквы, цифры и специальные символы: !@#$%^&*()_+-="
        )

    if not re.search(r"[a-zA-Z]", value):
        raise ValueError("Пароль должен содержать хотя бы одну латинскую букву")

    if not re.search(r"[0-9]", value):
        raise ValueError("Пароль должен содержать хотя бы одну цифру")

    return value


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


class BaseUserSchema(BaseModel):
    email: EmailStr
    role: UserRole = Field(default=UserRole.USER)


class UserCreateSchema(BaseUserSchema):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return validate_password(value=value)


class UserOut(BaseUserSchema):
    id: int
    team_id: int | None = Field(default=None)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class AdminUserOut(UserOut): ...


class ManagerUserOut(UserOut): ...


class UserUpdateSchema(BaseModel):
    password: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if value is None:
            return value
        return validate_password(value=value)
