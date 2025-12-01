from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


class EvaluationModel(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), unique=True)
    evaluator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    task: Mapped["TaskModel"] = relationship(back_populates="evaluation")
    evaluator: Mapped["UserModel"] = relationship(
        foreign_keys=[evaluator_id], back_populates="evaluations"
    )
    user: Mapped["UserModel"] = relationship(
        foreign_keys=[user_id], back_populates="received_evaluations"
    )

    def __str__(self):
        return f"Evaluation #{self.id} — Score: {self.score} — User: {self.user_id} — Task: {self.task_id}"
