from dataclasses import dataclass
from src.services.hash import BaseHashService
from src.schemas.user import UserUpdateSchema, UserOut
from src.repositories.user import BaseUserRepository
from src.models.user import UserModel
from src.exceptions.user import UserAlreadyExists




@dataclass
class UpdateUserUseCase:
    _user_repository: BaseUserRepository
    _hash_service: BaseHashService

    async def execute(self, updated_user: UserUpdateSchema, user: UserModel) -> UserOut:

        if updated_user.password:
            hashed_password: str = self._hash_service.get_password_hash(password=updated_user.password)
            user.hashed_password = hashed_password
        

        if updated_user.email:
   
            email_exists: bool = await self._user_repository.email_exists(email=updated_user.email)
            if email_exists:
                if updated_user.email != user.email:
                    raise UserAlreadyExists()
            
            user.email = updated_user.email
            
        await self._user_repository.save(user=user)
        return UserOut.model_validate(user)