from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.schemas.task import TaskStatus



class TaskModel(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[str] = mapped_column(default=TaskStatus.OPEN)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))

    author: Mapped['UserModel'] = relationship(
        foreign_keys=[author_id], 
        back_populates='authored_tasks'
    )
    assignee: Mapped['UserModel | None'] = relationship(
        foreign_keys=[assignee_id],
        back_populates='assigned_tasks'
    )
    team: Mapped['TeamModel'] = relationship(back_populates='tasks')
    comments: Mapped[list['TaskCommentModel']] = relationship(
        back_populates='task',
        cascade='all, delete-orphan'
    )

    evaluation: Mapped['EvaluationModel | None'] = relationship(
        back_populates='task',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def __str__(self) -> str:
        return f'Task: {self.id}: {self.title}'


class TaskCommentModel(Base):
    __tablename__ = 'task_comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))

    author: Mapped['UserModel'] = relationship(back_populates='task_comments')
    task: Mapped['TaskModel'] = relationship(back_populates='comments')

    def __str__(self) -> str:
        return f'TaskComment: {self.id}: {self.text[:10]}'