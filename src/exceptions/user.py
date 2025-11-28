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



class UnauthorizedException(BaseAppException):
    status_code = status.HTTP_401_UNAUTHORIZED

    @property
    def message(self) -> str:
        return 'Пользователь не авторизован.'
    

class ForbiddenException(BaseAppException):
    status_code = status.HTTP_403_FORBIDDEN

    @property
    def message(self) -> str:
        return 'Недостаточно прав.'
    


class AlreadyInTeamException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Пользователь уже состоит в команде.'
    

class UserNotInTeamException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Пользователь не состоит в команде.'
    

class InvalidRoleException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Недопустимая роль пользователя.'
    

class ManagerNotInTeamException(BaseAppException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message(self) -> str:
        return 'Менеджер не состоит в команде.'