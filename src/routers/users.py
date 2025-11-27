from typing import Annotated
from fastapi import APIRouter, Path, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.models.user import UserModel
from src.schemas.user import AdminUserOut, UserUpdateSchema, UserOut
from src.use_cases.user.update_user import UpdateUserUseCase
from src.use_cases.user.delete import DeleteUserUseCase
from src.use_cases.admin.delete_user import DeleteUserByAdminUseCase


router: APIRouter = APIRouter()



@router.patch(
    '/',
    summary='Обновление пользователя',
    description='Обновляет email и/или пароль пользователя',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Данные пользователя успешно обновлены',
            'model': UserOut,
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Email уже занят другим пользователем',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Пользователь не авторизован',
        }
    },
)
@inject
async def update_user(
    updated_data: UserUpdateSchema,
    user: Depends[UserModel],
    use_case: Depends[UpdateUserUseCase],
) -> UserOut:

    return await use_case.execute(updated_user=updated_data, user=user)



@router.delete(
    '/',
    summary='Удаление пользователя',
    description='Мягкое удаление пользователя',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            'description': 'Пользователь успешно удален',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Пользователь не авторизован',
        },
        status.HTTP_404_NOT_FOUND: {
            'description': 'Пользователь не найден',
        },
    },
)
@inject
async def delete_user(
    user: Depends[UserModel],
    use_case: Depends[DeleteUserUseCase]
) -> None:
    await use_case.execute(user=user)




@router.delete(
    '/users/{user_id}',
    description='[ADMIN] Удаление пользователя по его ID.',
    summary='Удалить пользователя',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Пользователь удален'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для администраторов'},
        status.HTTP_404_NOT_FOUND: {'description': 'Пользователь не найден'},
    },
)
@inject
async def delete_user_by_admin(
    user_id: Annotated[int, Path(description='ID пользователя, которого нужно удалить')],
    admin: Depends[AdminUserOut],
    use_case: Depends[DeleteUserByAdminUseCase],
) -> None:
    
    await use_case.execute(user_id=user_id)