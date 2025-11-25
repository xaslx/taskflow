from fastapi import APIRouter, status, Path
from typing import Annotated
from dishka.integrations.fastapi import inject, FromDishka as Depends

from src.schemas.user import AdminUserOut
from src.schemas.team import CreateTeamSchema, TeamOut
from src.use_cases.admin.create_team import CreateTeamUseCase
from src.use_cases.admin.delete_user import DeleteUserByAdminUseCase



router: APIRouter = APIRouter()


@router.delete(
    '/users/{user_id}',
    description='Удаление пользователя по его ID. Только для администраторов',
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



@router.post(
    '/teams',
    description='Создаёт команду',
    summary='Создать команду',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для администраторов'},
    },
)
@inject
async def create_team(
    admin: Depends[AdminUserOut],
    team: CreateTeamSchema,
    use_case: Depends[CreateTeamUseCase],
) -> TeamOut:
    
    return await use_case.execute(team=team)