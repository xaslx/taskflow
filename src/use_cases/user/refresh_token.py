from dataclasses import dataclass
from src.services.jwt import JWTService
from fastapi import HTTPException, status


@dataclass
class RefreshTokenUseCase:
    _jwt_service: JWTService

    async def execute(self, refresh_token: str) -> str:
        try:
            new_access_token: str | None = self._jwt_service.refresh_access_token(
                refresh_token
            )
            return new_access_token
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
