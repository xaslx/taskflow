from src.exceptions.base import BaseAppException
from fastapi import status


class UserAlreadyExists(BaseAppException):
    status_code = status.HTTP_409_CONFLICT

    @property
    def message(self) -> str:
        return 'Пользователь уже зарегистрирован.'


class IncorrectEmailOrPasswordException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return 'Неверный email или пароль.'


class UserNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND

    @property
    def message(self) -> str:
        return 'Пользователь не найден.'


