from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


class MeetingModel(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    participant_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[])
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )

    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    organizer: Mapped["UserModel"] = relationship(back_populates="organized_meetings")
    team: Mapped["TeamModel"] = relationship(back_populates="meetings")

    def __str__(self) -> str:
        return f"Meeting: {self.id}: {self.title}"
