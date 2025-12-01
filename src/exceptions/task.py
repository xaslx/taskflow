from src.exceptions.base import BaseAppException
from fastapi import status


class TaskNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND

    @property
    def message(self) -> str:
        return "Задача не найдена."


class TaskNotCompletedException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return "Можно оценивать только завершенные задачи."


class TaskNotAssigneeException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return "Задача не имеет исполнителя."
