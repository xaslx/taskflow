from src.exceptions.base import BaseAppException
from fastapi import status


class TimeConflictException(BaseAppException):
    status_code = status.HTTP_409_CONFLICT

    @property
    def message(self) -> str:
        return 'Время встречи пересекается с другими событиями.'
    


class MeetingNotFoundException(BaseAppException):
    status_code = status.HTTP_404_NOT_FOUND

    @property
    def message(self) -> str:
        return 'Встреча не найдена.'