from dataclasses import dataclass
from src.schemas.token import TokenResponse
from src.schemas.user import UserLoginSchema
from src.exceptions.user import UserNotFoundException
from src.models.user import UserModel
from src.repositories.user import BaseUserRepository
from src.services.jwt import JWTService
from src.services.auth import BaseAuthService
from datetime import datetime



@dataclass
class LoginUserUseCase:
    _jwt_service: JWTService
    _auth_service: BaseAuthService
    _user_repository: BaseUserRepository


    async def execute(self, credentials: UserLoginSchema) -> TokenResponse:
        user: UserModel | None = await self._auth_service.authenticate_user(email=credentials.email, password=credentials.password)
        
        if not user:
            raise UserNotFoundException()
        
        access_token, refresh_token = self._jwt_service.create_tokens({'sub': str(user.id)})
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
        