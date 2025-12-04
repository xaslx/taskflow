from datetime import date
from fastapi import APIRouter, Query, status, Request
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.schemas.calendar import CalendarOut
from src.use_cases.user.calendar import DayCalendarUseCase, MonthCalendarUseCase
from src.models.user import UserModel
from typing import Annotated
from fastapi.templating import Jinja2Templates


router = APIRouter()



@router.get(
    '/day',
    description='Получение календаря с задачами и встречами на конкретную дату',
    summary='Получить календарь задач и встреч на конкретную дату',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Успешное получение календаря с задачами и встречами",
            "model": CalendarOut,
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Не авторизован"},
    },

)
@inject
async def get_day_calendar(
    user: Depends[UserModel],
    use_case: Depends[DayCalendarUseCase],
    date: Annotated[date, Query(description="Дата в формате YYYY-MM-DD")] = None,
) -> CalendarOut:
    

    return await use_case.execute(user_id=user.id, date=date)


@router.get(
    '/month',
    description='Получение календаря с задачами и встречами на весь месяц',
    summary='Получить календарь задач и встреч на весь месяц',
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Успешное получение календаря с задачами и встречами",
            "model": CalendarOut,
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Не авторизован"},
    },
)
@inject
async def get_month_calendar(
    user: Depends[UserModel],
    use_case: Depends[MonthCalendarUseCase], 
    year: Annotated[int, Query(ge=2000, le=2100, description="Год (например, 2025)")] = None,
    month: Annotated[int, Query(ge=1, le=12, description="Месяц (1-12)")] = None,
) -> CalendarOut:

    return await use_case.execute(
        user_id=user.id,
        year=year,
        month=month
    )


@router.get(
    '/'
)
@inject
async def get_calendar(
    request: Request,
    template: Depends[Jinja2Templates],
    user: Depends[UserModel],
):
    
    return template.TemplateResponse(
        request=request,
        name='calendar.html',
        context={'user': user},
    )