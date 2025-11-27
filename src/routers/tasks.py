from fastapi import APIRouter, status
from src.schemas.task import TaskCommentCreate, TaskCreate, TaskOut, TaskUpdate
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.schemas.user import ManagerUserOut
from src.use_cases.manager.create_task import CreateTaskUseCase
from src.use_cases.manager.get_all_tasks import GetAllTasksUseCase



router: APIRouter = APIRouter()



@router.post(
    '/',
    description='[MANAGER] Создание задачи руководителем',
    summary='Создать задачу',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Успешное создание задачи',
            'model': TaskOut,
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_404_NOT_FOUND: {'description': 'Команда не найдена'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для менеджеров'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Менеджер не состоит в команде.'}
    },
)
@inject
async def create_task(
    manager: Depends[ManagerUserOut],
    task: TaskCreate,
    use_case: Depends[CreateTaskUseCase]
) -> TaskOut:
    
    return await use_case.execute(task=task, author_id=manager.id)


@router.get(
    '/',
    description='[MANAGER] Получение списка задач в команде, где состоит менеджер',
    summary='Получение списка задач',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Успешное получение списка задач',
            'model': list[TaskOut],
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для менеджеров'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Менеджер не состоит в команде.'}
    },
)
@inject
async def get_all_tasks(
    manager: Depends[ManagerUserOut],
    use_case: Depends[GetAllTasksUseCase],
) -> list[TaskOut]:
    
    return await use_case.execute(team_id=manager.team_id)