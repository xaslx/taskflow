from fastapi import APIRouter, status, Path
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.schemas.meeting import MeetingCreate, MeetingOut
from src.schemas.user import ManagerUserOut
from src.use_cases.manager.create_meeting import CreateMeetingUseCase
from src.models.user import UserModel
from src.use_cases.user.get_user_meetings import GetUserMeetingsUseCase
from typing import Annotated
from src.use_cases.manager.delete_meeting import DeleteMeetingUseCase



router: APIRouter = APIRouter()


@router.post(
    '/',
    description='[MANAGER] Создание встречи',
    summary='Создать встречу',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Встреча успешно создана',
            'model': MeetingOut,
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для менеджеров'},
        status.HTTP_409_CONFLICT: {'description': 'Время встречи пересекается с другими событиями'},
    },
)
@inject
async def create_meeting(
    manager: Depends[ManagerUserOut],
    meeting: MeetingCreate,
    use_case: Depends[CreateMeetingUseCase],
) -> MeetingOut:
    
    return await use_case.execute(meeting_data=meeting, organizer_id=manager.id)



@router.get(
    '/',
    description='Получение всех встреч пользователя',
    summary='Получить мои встречи',
    responses={
        status.HTTP_200_OK: {
            'description': 'Список встреч пользователя',
            'model': list[MeetingOut],
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
    },
)
@inject
async def get_user_meetings(
    user: Depends[UserModel],
    use_case: Depends[GetUserMeetingsUseCase],
) -> list[MeetingOut]:
    
    return await use_case.execute(user_id=user.id)



@router.delete(
    '/{meeting_id}',
    description='[MANAGER] Удаление встречи',
    summary='Удалить встречу',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Встреча удалена'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для менеджеров'},
        status.HTTP_404_NOT_FOUND: {'description': 'Встреча не найдена'},
    },
)
@inject
async def delete_meeting(
    meeting_id: Annotated[int, Path()],
    user: Depends[ManagerUserOut],
    use_case: Depends[DeleteMeetingUseCase],
) -> None:
    
    await use_case.execute(
        meeting_id=meeting_id,
        user_id=user.id,
        user_team_id=user.team_id
    )