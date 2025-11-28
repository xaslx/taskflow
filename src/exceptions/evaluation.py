from src.exceptions.base import BaseAppException
from fastapi import status


class EvaluationAlreadyExistsException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST
    
    @property
    def message(self) -> str:
        return 'Оценка для этой задачи уже существует.'