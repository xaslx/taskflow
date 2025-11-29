from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.services.auth import BaseAuthService


router: APIRouter = APIRouter()



@router.get(
    '/',
    description='Главная страница',
    summary='Главная страница',
)
@inject
async def main_page(
    request: Request,
    template: Depends[Jinja2Templates],
    auth_service: Depends[BaseAuthService]
):

    user_access_token: str | None = request.cookies.get('access_token', None)

    if not user_access_token:
        user = None
    else:
        try:
            user = await auth_service.get_current_user(token=user_access_token)
        except Exception:
            user = None

    return template.TemplateResponse(
        request=request,
        name='index.html',
        context={'user': user}
    )