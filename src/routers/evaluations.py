from fastapi import APIRouter, status
from src.schemas.user import ManagerUserOut
from src.models.user import UserModel
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.schemas.evaluation import EvaluationCreate, EvaluationOut
from src.use_cases.user.get_all_evaluations import GetAllEvaluationsUseCase
from src.use_cases.manager.create_evaluation import CreateEvaluationUseCase


router: APIRouter = APIRouter()


@router.get(
    '/',
    description='Получение всех оценок пользователя',
    summary='Получить все оценки',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Успешное получение оценок',
            'model': list[EvaluationOut],
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
    },
)
@inject
async def get_all_evaluations(
    user: Depends[UserModel],
    use_case: Depends[GetAllEvaluationsUseCase]
) -> list[EvaluationOut]:
    
    return await use_case.execute(user_id=user.id)



@router.post(
    '/',
    description='[MANAGER] Выставление оценки за выполненную задачу',
    summary='Поставить оценку',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Оценка успешно поставлена',
            'model': EvaluationOut,
        },
        status.HTTP_401_UNAUTHORIZED: {'description': 'Не авторизован'},
        status.HTTP_403_FORBIDDEN: {'description': 'Недостаточно прав. Только для менеджеров'},
        status.HTTP_404_NOT_FOUND: {'description': 'Задача не найдена'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Невозможно оценить задачу'},
    },
)
@inject
async def create_evaluation(
    evaluation: EvaluationCreate,
    manager: Depends[ManagerUserOut],
    use_case: Depends[CreateEvaluationUseCase],
) -> EvaluationOut:
    
    return await use_case.execute(
        evaluation=evaluation,
        evaluator_id=manager.id,
        team_id=manager.team_id
    )