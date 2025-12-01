from src.exceptions.base import BaseAppException
from fastapi import status


class TokenExpiredException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return "Токен истёк"


class IncorrectTokenException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return "Невалидный токен"
