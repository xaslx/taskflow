from collections.abc import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.services.auth import BaseAuthService, AuthServiceImpl
from src.config import Config
from src.database.postgres import new_engine_and_session_maker
from src.use_cases.user.register import RegisterUserUseCase
from src.repositories.user import BaseUserRepository, SQLAlchemyUserRepository
from src.services.hash import BaseHashService, BCryptHashService
from src.services.jwt import JWTService, JWTServiceImpl
from src.use_cases.user.login import LoginUserUseCase
from src.use_cases.user.refresh_token import RefreshTokenUseCase
from src.models.user import UserModel
from src.use_cases.user.update_user import UpdateUserUseCase
from src.use_cases.user.delete import DeleteUserUseCase
from src.exceptions.user import (
    ForbiddenException,
    ManagerNotInTeamException,
    UnauthorizedException,
)
from src.schemas.user import ManagerUserOut, UserRole, AdminUserOut
from src.use_cases.admin.delete_user import DeleteUserByAdminUseCase
from src.repositories.team import BaseTeamRepository, SQLAlchemyTeamRepository
from src.use_cases.admin.create_team import CreateTeamUseCase
from src.use_cases.user.join_team import JoinTeamByCodeUseCase
from src.use_cases.admin.get_all_teams import GetAllTeamsUseCase
from src.use_cases.admin.get_team_info import GetTeamInfoUseCase
from src.use_cases.admin.team_manager import (
    AddTeamMemberUseCase,
    ChangeUserRoleUseCase,
    DeleteTeamMemberUseCase,
)
from src.use_cases.manager.create_task import CreateTaskUseCase
from src.repositories.task import BaseTaskRepository, SQLAlchemyTaskRepository
from src.use_cases.manager.get_all_tasks import GetAllTasksUseCase
from src.use_cases.manager.get_by_task_by_id import GetTaskByIdUseCase
from src.use_cases.manager.delete_task_by_id import DeleteTaskByIdUseCase
from src.use_cases.manager.update_task import UpdateTaskUseCase
from src.use_cases.user.add_task_comment import CreateCommentUseCase
from src.repositories.task import (
    BaseTaskCommentRepository,
    SQLAlchemyTaskCommentRepository,
)
from src.repositories.evaluation import (
    BaseEvaluationRepository,
    SQLAlchemyEvaluationRepository,
)
from src.use_cases.user.get_all_evaluations import GetAllEvaluationsUseCase
from src.use_cases.manager.create_evaluation import CreateEvaluationUseCase
from src.repositories.meeting import BaseMeetingRepository, SQLAlchemyMeetingRepository
from src.use_cases.manager.create_meeting import CreateMeetingUseCase
from src.use_cases.user.get_user_meetings import GetUserMeetingsUseCase
from src.use_cases.manager.delete_meeting import DeleteMeetingUseCase
from fastapi.templating import Jinja2Templates


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_engine_and_session_maker(config)[0]

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_jinja_template(self) -> Jinja2Templates:
        template: Jinja2Templates = Jinja2Templates(directory="src/static/templates")
        return template

    # services
    @provide(scope=Scope.REQUEST)
    def get_hash_service(self) -> BaseHashService:
        return BCryptHashService()

    @provide(scope=Scope.REQUEST)
    def get_jwt_service(self, config: Config) -> JWTService:
        return JWTServiceImpl(config=config)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(
        self,
        user_repository: BaseUserRepository,
        hash_service: BaseHashService,
        jwt_service: JWTService,
    ) -> BaseAuthService:

        return AuthServiceImpl(
            _user_repository=user_repository,
            _hash_service=hash_service,
            _jwt_service=jwt_service,
        )

    # repositories
    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(_session=session)

    @provide(scope=Scope.REQUEST)
    def get_team_repository(self, session: AsyncSession) -> BaseTeamRepository:
        return SQLAlchemyTeamRepository(_session=session)

    @provide(scope=Scope.REQUEST)
    def get_task_repository(self, session: AsyncSession) -> BaseTaskRepository:
        return SQLAlchemyTaskRepository(_session=session)

    @provide(scope=Scope.REQUEST)
    def get_task_comment_repository(
        self, session: AsyncSession
    ) -> BaseTaskCommentRepository:
        return SQLAlchemyTaskCommentRepository(_session=session)

    @provide(scope=Scope.REQUEST)
    def get_evaluation_repository(
        self, session: AsyncSession
    ) -> BaseEvaluationRepository:
        return SQLAlchemyEvaluationRepository(_session=session)

    @provide(scope=Scope.REQUEST)
    def get_meeting_repository(self, session: AsyncSession) -> BaseMeetingRepository:
        return SQLAlchemyMeetingRepository(_session=session)

    # use cases
    @provide(scope=Scope.REQUEST)
    def get_register_user_use_case(
        self, user_repository: BaseUserRepository, hash_service: BaseHashService
    ) -> RegisterUserUseCase:
        return RegisterUserUseCase(
            _user_repository=user_repository, _hash_service=hash_service
        )

    @provide(scope=Scope.REQUEST)
    def get_login_user_use_case(
        self,
        user_repository: BaseUserRepository,
        auth_service: BaseAuthService,
        jwt_service: JWTService,
    ) -> LoginUserUseCase:

        return LoginUserUseCase(
            _jwt_service=jwt_service,
            _auth_service=auth_service,
            _user_repository=user_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_refresh_token_use_case(
        self, jwt_service: JWTService
    ) -> RefreshTokenUseCase:

        return RefreshTokenUseCase(_jwt_service=jwt_service)

    @provide(scope=Scope.REQUEST)
    def get_update_user_use_case(
        self,
        hash_service: BaseHashService,
        user_repository: BaseUserRepository,
    ) -> UpdateUserUseCase:

        return UpdateUserUseCase(
            _hash_service=hash_service,
            _user_repository=user_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_delete_user_use_case(
        self, user_repository: BaseUserRepository
    ) -> DeleteUserUseCase:
        return DeleteUserUseCase(_user_repository=user_repository)

    @provide(scope=Scope.REQUEST)
    def get_delete_user_by_admin_use_case(
        self, user_repository: BaseUserRepository
    ) -> DeleteUserByAdminUseCase:

        return DeleteUserByAdminUseCase(_user_repository=user_repository)

    @provide(scope=Scope.REQUEST)
    def get_create_team_use_case(
        self, team_repository: BaseTeamRepository
    ) -> CreateTeamUseCase:
        return CreateTeamUseCase(_team_repository=team_repository)

    @provide(scope=Scope.REQUEST)
    def get_join_team_by_code_use_case(
        self,
        user_repository: BaseUserRepository,
        team_repository: BaseTeamRepository,
    ) -> JoinTeamByCodeUseCase:

        return JoinTeamByCodeUseCase(
            _user_repository=user_repository,
            _team_repository=team_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_all_teams_use_case(
        self,
        team_repository: BaseTeamRepository,
    ) -> GetAllTeamsUseCase:

        return GetAllTeamsUseCase(_team_repository=team_repository)

    @provide(scope=Scope.REQUEST)
    def get_team_info_use_case(
        self,
        team_repository: BaseTeamRepository,
    ) -> GetTeamInfoUseCase:

        return GetTeamInfoUseCase(_team_repository=team_repository)

    @provide(scope=Scope.REQUEST)
    def get_add_team_member_use_case(
        self,
        user_repository: BaseUserRepository,
        team_repository: BaseTeamRepository,
    ) -> AddTeamMemberUseCase:

        return AddTeamMemberUseCase(
            _user_repository=user_repository,
            _team_repository=team_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_delete_team_member_use_case(
        self,
        user_repository: BaseUserRepository,
        team_repository: BaseTeamRepository,
    ) -> DeleteTeamMemberUseCase:

        return DeleteTeamMemberUseCase(
            _user_repository=user_repository,
            _team_repository=team_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_change_user_role_use_case(
        self,
        user_repository: BaseUserRepository,
        team_repository: BaseTeamRepository,
    ) -> ChangeUserRoleUseCase:

        return ChangeUserRoleUseCase(
            _user_repository=user_repository,
            _team_repository=team_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_create_task_use_case(
        self,
        task_repository: BaseTaskRepository,
        team_repository: BaseTeamRepository,
        user_repository: BaseUserRepository,
    ) -> CreateTaskUseCase:

        return CreateTaskUseCase(
            _task_repository=task_repository,
            _team_repository=team_repository,
            _user_repository=user_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_all_tasks(
        self,
        task_repository: BaseTaskRepository,
    ) -> GetAllTasksUseCase:

        return GetAllTasksUseCase(_task_repository=task_repository)

    @provide(scope=Scope.REQUEST)
    def get_task_by_id_use_case(
        self,
        task_repository: BaseTaskRepository,
    ) -> GetTaskByIdUseCase:

        return GetTaskByIdUseCase(_task_repository=task_repository)

    @provide(scope=Scope.REQUEST)
    def get_delete_task_by_id_use_case(
        self,
        task_repository: BaseTaskRepository,
    ) -> DeleteTaskByIdUseCase:

        return DeleteTaskByIdUseCase(_task_repository=task_repository)

    @provide(scope=Scope.REQUEST)
    def get_update_task_use_case(
        self,
        task_repository: BaseTaskRepository,
    ) -> UpdateTaskUseCase:

        return UpdateTaskUseCase(_task_repository=task_repository)

    @provide(scope=Scope.REQUEST)
    def get_create_task_comment_use_case(
        self,
        task_repository: BaseTaskRepository,
        task_comment_repository: BaseTaskCommentRepository,
    ) -> CreateCommentUseCase:

        return CreateCommentUseCase(
            _task_repository=task_repository,
            _task_comment_repository=task_comment_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_all_evaluations_use_case(
        self,
        evaluation_repository: BaseEvaluationRepository,
    ) -> GetAllEvaluationsUseCase:

        return GetAllEvaluationsUseCase(_evaluation_repository=evaluation_repository)

    @provide(scope=Scope.REQUEST)
    def get_create_evaluation(
        self,
        evaluation_repository: BaseEvaluationRepository,
        task_repository: BaseTaskRepository,
    ) -> CreateEvaluationUseCase:

        return CreateEvaluationUseCase(
            _evaluation_repository=evaluation_repository,
            _task_repository=task_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_create_meeting_use_case(
        self,
        meeting_repository: BaseMeetingRepository,
        user_repository: BaseUserRepository,
        team_repository: BaseTeamRepository,
    ) -> CreateMeetingUseCase:

        return CreateMeetingUseCase(
            _meeting_repository=meeting_repository,
            _user_repository=user_repository,
            _team_repository=team_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_user_meetings_use_case(
        self,
        meeting_repository: BaseMeetingRepository,
    ) -> GetUserMeetingsUseCase:

        return GetUserMeetingsUseCase(_meeting_repository=meeting_repository)

    @provide(scope=Scope.REQUEST)
    def get_delete_meeting_use_case(
        self,
        meeting_repository: BaseMeetingRepository,
    ) -> DeleteMeetingUseCase:

        return DeleteMeetingUseCase(_meeting_repository=meeting_repository)

    @provide(scope=Scope.REQUEST)
    def get_token(self, request: Request) -> str:

        token: str = request.cookies.get("access_token")

        if not token:
            return None
        return token

    @provide(scope=Scope.REQUEST)
    async def get_current_user_dependency(
        self,
        auth_service: BaseAuthService,
        token: str,
    ) -> UserModel:

        if not token:
            raise UnauthorizedException()

        return await auth_service.get_current_user(token=token)

    @provide(scope=Scope.REQUEST)
    async def get_admin_user_dependency(
        self,
        current_user: UserModel,
    ) -> AdminUserOut:

        if current_user.role != UserRole.ADMIN:
            raise ForbiddenException()
        return AdminUserOut.model_validate(current_user)

    @provide(scope=Scope.REQUEST)
    async def get_manager_user_dependency(
        self,
        current_user: UserModel,
    ) -> ManagerUserOut:

        if current_user.role != UserRole.MANAGER:
            raise ForbiddenException()

        if not current_user.team_id:
            raise ManagerNotInTeamException()

        return ManagerUserOut.model_validate(current_user)
