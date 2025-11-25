from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = 'admin'
    USER = 'user'
    MANAGER = 'manager'


class BaseUserSchema(BaseModel):
    email: EmailStr
    role: UserRole = Field(default=UserRole.USER)


class UserCreateSchema(BaseUserSchema):
    password: str = Field(min_length=6, max_length=20, description='Пароль от 6 до 20 символов')

class UserOut(BaseUserSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str