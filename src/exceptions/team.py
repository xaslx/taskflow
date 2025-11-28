from src.exceptions.base import BaseAppException
from fastapi import status


class TeamNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND

    @property
    def message(self) -> str:
        return 'Команда не найдена'