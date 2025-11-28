from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TeamModel(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    code: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list['UserModel']] = relationship(
        'UserModel',
        back_populates='team',
        passive_deletes=True
    )


    tasks: Mapped[list['TaskModel']] = relationship(
        back_populates='team',
        cascade='all, delete-orphan'
    )