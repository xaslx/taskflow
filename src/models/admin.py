from src.models.user import UserModel
from src.models.evaluation import EvaluationModel
from src.models.meeting import MeetingModel
from src.models.task import TaskModel, TaskCommentModel
from src.models.team import TeamModel
from sqladmin import ModelView


class UserAdmin(ModelView, model=UserModel):
    column_list = [UserModel.id, UserModel.email, UserModel.role, UserModel.created_at]
    column_searchable_list = [UserModel.email]
    column_sortable_list = [UserModel.id, UserModel.email, UserModel.created_at]


class TeamAdmin(ModelView, model=TeamModel):
    column_list = [TeamModel.id, TeamModel.name]
    column_searchable_list = [TeamModel.name]
    column_sortable_list = [TeamModel.id, TeamModel.name]


class TaskAdmin(ModelView, model=TaskModel):
    column_list = [
        TaskModel.id,
        TaskModel.title,
        TaskModel.author_id,
        TaskModel.assignee_id,
        TaskModel.status,
    ]
    column_searchable_list = [TaskModel.title]
    column_sortable_list = [TaskModel.id, TaskModel.title, TaskModel.status]


class TaskCommentAdmin(ModelView, model=TaskCommentModel):
    column_list = [
        TaskCommentModel.id,
        TaskCommentModel.task_id,
        TaskCommentModel.author_id,
        TaskCommentModel.created_at,
    ]
    column_searchable_list = []
    column_sortable_list = [TaskCommentModel.id, TaskCommentModel.created_at]


class EvaluationAdmin(ModelView, model=EvaluationModel):
    column_list = [
        EvaluationModel.id,
        EvaluationModel.user_id,
        EvaluationModel.evaluator_id,
        EvaluationModel.score,
    ]
    column_searchable_list = []
    column_sortable_list = [EvaluationModel.id, EvaluationModel.score]


class MeetingAdmin(ModelView, model=MeetingModel):
    column_list = [
        MeetingModel.id,
        MeetingModel.title,
        MeetingModel.organizer_id,
        MeetingModel.start_time,
        MeetingModel.end_time,
    ]
    column_searchable_list = [MeetingModel.title]
    column_sortable_list = [
        MeetingModel.id,
        MeetingModel.start_time,
        MeetingModel.end_time,
    ]
