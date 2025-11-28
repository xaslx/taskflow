from fastapi import APIRouter, status, Path
from src.models.user import UserModel
from src.schemas.task import TaskCommentCreate, TaskCommentOut, TaskCreate, TaskOut, TaskUpdate
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.schemas.user import ManagerUserOut
from src.use_cases.manager.create_task import CreateTaskUseCase
from src.use_cases.manager.get_all_tasks import GetAllTasksUseCase
from src.use_cases.manager.get_by_task_by_id import GetTaskByIdUseCase
from typing import Annotated
from src.use_cases.manager.delete_task_by_id import DeleteTaskByIdUseCase
from src.use_cases.manager.update_task import UpdateTaskUseCase
from src.use_cases.user.add_task_comment import CreateCommentUseCase



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



@router.get(
    '/{task_id}',
    description='[MANAGER] Получение задачи по ID',
    summary='Получить задачу по ID',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Успешное получение задачи',
            'model': TaskOut,
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для менеджеров'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Менеджер не состоит в команде.'}
    },
)
@inject
async def get_task_by_id(
    task_id: Annotated[int, Path()],
    manager: Depends[ManagerUserOut],
    use_case: Depends[GetTaskByIdUseCase],
) -> TaskOut | None:
    
    return await use_case.execute(task_id=task_id, team_id=manager.team_id)


@router.delete(
    '/{task_id}',
    description='[MANAGER] Удаление задачи по ID',
    summary='Удалить задачу по ID',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Успешное удаление задачи',},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Менеджер не состоит в команде.'}
    },
)
@inject
async def delete_task_by_id(
    task_id: Annotated[int, Path()],
    manager: Depends[ManagerUserOut],
    use_case: Depends[DeleteTaskByIdUseCase],
) -> None:
    
    return await use_case.execute(
        task_id=task_id,
        user_id=manager.id,
        user_team_id=manager.team_id
    )



@router.patch(
    '/{task_id}',
    description='[MANAGER] Изменение задачи',
    summary='Изменить задачу',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Успешное обновление задачи',
            'model': TaskOut,
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав.'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Менеджер не состоит в команде.'}
    },
)
@inject
async def update_task(
    task_id: Annotated[int, Path()],
    updated_task: TaskUpdate,
    manager: Depends[ManagerUserOut],
    use_case: Depends[UpdateTaskUseCase]
) -> TaskOut:
    
    return await use_case.execute(
        updated_task=updated_task,
        task_id=task_id,
        team_id=manager.team_id,
        author_id=manager.id
    )



@router.post(
    '/{task_id}/comments',
    description='Добавление комментария к задаче',
    summary='Добавить комментарий',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Комментарий добавлен',
            'model': TaskCommentOut,
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_404_NOT_FOUND: {'description': 'Задача не найдена'},
        status.HTTP_403_FORBIDDEN: {'description': 'Нет доступа к задаче'},
    },
)
@inject
async def create_comment(
    task_id: Annotated[int, Path()],
    comment: TaskCommentCreate,
    user: Depends[UserModel],
    use_case: Depends[CreateCommentUseCase],
) -> TaskCommentOut:
    
    return await use_case.execute(
        task_id=task_id,
        comment=comment,
        author_id=user.id,
        team_id=user.team_id
    )