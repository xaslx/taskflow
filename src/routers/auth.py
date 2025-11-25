from fastapi import APIRouter, status, Response, Request, HTTPException
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.schemas.response import SuccessResponse
from src.schemas.user import UserCreateSchema, UserOut, UserLoginSchema
from src.use_cases.user.register import RegisterUserUseCase
from src.schemas.token import TokenResponse
from src.use_cases.user.login import LoginUserUseCase
from src.use_cases.user.refresh_token import RefreshTokenUseCase



router: APIRouter = APIRouter()


@router.post(
    '/register',
    summary='Регистрация пользователя',
    description='Создаёт нового пользователя и возвращает его данные',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Пользователь успешно зарегистрирован',
            'model': UserOut,
        },
        status.HTTP_409_CONFLICT: {
            'description': 'Пользователь уже зарегистрирован',
        },
    },
)
@inject
async def register_user(
    user: UserCreateSchema,
    use_case: Depends[RegisterUserUseCase],
) -> UserOut:
    

    return await use_case.execute(new_user=user)




@router.post(
    '/login',
    summary='Авторизация пользователя',
    description='Проверяет email и пароль, возвращает токен и данные пользователя.',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Успешная авторизация',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Неверный email или пароль',
        }
    }
)

@inject
async def login_user(
    credentials: UserLoginSchema,
    use_case: Depends[LoginUserUseCase],
    response: Response
) -> TokenResponse:
    
    tokens: TokenResponse = await use_case.execute(credentials)
    response.set_cookie(
        key='access_token',
        value=tokens.access_token,
        httponly=True,

    )
    response.set_cookie(
        key='refresh_token',
        value=tokens.refresh_token,
        httponly=True,

    )
    return tokens


@router.post(
    '/refresh-token',
    status_code=status.HTTP_200_OK,
    description='Эндпоинт для обновления access token',
    responses={
        status.HTTP_200_OK: {
            'model': SuccessResponse,
            'description': 'Access token успешно обновлён',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Refresh token отсутствует или недействителен',
        },
    },
)
@inject
async def refresh_token(
    response: Response,
    request: Request,
    use_case: Depends[RefreshTokenUseCase],
) -> SuccessResponse:
    token: str | None = request.cookies.get('refresh_token')
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token not found'
        )

    new_access_token: str = await use_case.execute(refresh_token=token)
    response.set_cookie(
        key='access_token', value=new_access_token, httponly=True
    )
    return SuccessResponse(detail='Access token успешно обновлён')



@router.post(
    '/logout',
    summary='Выход пользователя',
    description='Удаляет access и refresh токены из куки.',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            'description': 'Пользователь успешно вышел',
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Пользователь не авторизован',
        }
    }
)
async def logout_user(response: Response) -> SuccessResponse:

    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return SuccessResponse(detail='Вы успешно вышли из системы')