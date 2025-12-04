from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from src.exceptions.base import BaseAppException
from src.config import Config
from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi as fastapi_integration
from src.routers import auth, users, teams, tasks, evaluations, meeting, main_page, calendar
from fastapi.middleware.cors import CORSMiddleware
from src.ioc import AppProvider
from sqladmin import Admin
from src.models.admin import (
    UserAdmin,
    TaskAdmin,
    TaskCommentAdmin,
    TeamAdmin,
    MeetingAdmin,
    EvaluationAdmin,
)
from src.database.postgres import new_engine_and_session_maker


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


def create_app_test() -> FastAPI:

    app: FastAPI = FastAPI()

    return app


def create_app() -> FastAPI:

    config: Config = Config()
    container: AsyncContainer = make_async_container(
        AppProvider(), context={Config: config}
    )

    app: FastAPI = FastAPI(
        title="TaskFlow",
        description="Система управления бизнесом",
        version="0.1",
    )
    _, engine = new_engine_and_session_maker(config=config)
    admin: Admin = Admin(app=app, engine=engine)
    admin.add_view(UserAdmin)
    admin.add_view(TeamAdmin)
    admin.add_view(TaskAdmin)
    admin.add_view(TaskCommentAdmin)
    admin.add_view(EvaluationAdmin)
    admin.add_view(MeetingAdmin)

    app.include_router(
        auth.router, prefix="/api/auth", tags=["Аутентификация и Авторизация"]
    )
    app.include_router(users.router, prefix="/api/users", tags=["Пользователи"])
    app.include_router(teams.router, prefix="/api/teams", tags=["Команда"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["Задачи"])
    app.include_router(evaluations.router, prefix="/api/evaluations", tags=["Оценки"])
    app.include_router(meeting.router, prefix="/api/meetings", tags=["Встречи"])
    app.include_router(main_page.router, prefix="", tags=["Главная страница"])
    app.include_router(calendar.router, prefix="/calendar", tags=["Календарь"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi_integration.setup_dishka(container=container, app=app)

    @app.exception_handler(BaseAppException)
    async def app_error_exception_handler(request: Request, exc: BaseAppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    return app
