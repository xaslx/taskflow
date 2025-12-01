from fastapi import status


class BaseAppException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def message() -> str:
        return f"Ошибка приложения"
