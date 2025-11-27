from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.schemas.user import UserRole




class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    role: Mapped[str] = mapped_column(default=UserRole.USER)
    hashed_password: Mapped[str]
    is_deleted: Mapped[bool] = mapped_column(default=False)

    team_id: Mapped[int | None] = mapped_column(
        ForeignKey('teams.id', ondelete='SET NULL'),
        nullable=True
    )
    team: Mapped['TeamModel'] = relationship('TeamModel', back_populates='users')