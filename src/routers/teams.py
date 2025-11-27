from fastapi import APIRouter, status, Path
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.models.user import UserModel
from src.schemas.team import JoinTeam, TeamOut, CreateTeamSchema, TeamOutWithUsers
from src.schemas.user import AdminUserOut, UserOut
from src.use_cases.admin.create_team import CreateTeamUseCase
from src.use_cases.user.join_team import JoinTeamByCodeUseCase
from src.use_cases.admin.get_all_teams import GetAllTeamsUseCase
from src.use_cases.admin.get_team_info import GetTeamInfoUseCase
from typing import Annotated


router: APIRouter = APIRouter()


@router.post(
    '/',
    description='[ADMIN] Создаёт команду',
    summary='Создать команду',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Команда успешно создана',
            'model': TeamOut,
        },
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



@router.post(
    '/join',
    description='Присоеденение к команде по коду',
    summary='Присоедениться к команде',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Пользователь присоеденился к команде',
            'model': UserOut,
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Пользователь уже состоит в команде'},
        status.HTTP_404_NOT_FOUND: {'description': 'Команда не найдена'},
    },
)
@inject
async def join_team_by_code(
    user: Depends[UserModel],
    code: JoinTeam,
    use_case: Depends[JoinTeamByCodeUseCase],
) -> UserOut:  
    
    return await use_case.execute(user=user, code=code.code)


@router.get(
    '/',
    description='[ADMIN] Получение всех команд',
    summary='Получить список всех команд',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Успешное получение списка команд',
            'model': list[TeamOut],
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Пользователь уже состоит в команде'},
        status.HTTP_404_NOT_FOUND: {'description': 'Команда не найдена'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для администраторов'},
    },
)
@inject
async def get_all_teams(
    admin: Depends[AdminUserOut],
    use_case: Depends[GetAllTeamsUseCase]
) -> list[TeamOut]:
    
    return await use_case.execute()



@router.get(
    '/{team_id}/members',
    description='[ADMIN] Получение информации о конкретной команде и ее участников',
    summary='Детальная информация о команде и ее участников',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Успешное получение инфо о команде',
            'model': TeamOutWithUsers,
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для администраторов'},
    },
)
@inject
async def get_team_info(
    team_id: Annotated[int, Path()],
    admin: Depends[AdminUserOut],
    use_case: Depends[GetTeamInfoUseCase],
) -> TeamOutWithUsers | None:
    
    return await use_case.execute(team_id=team_id)