from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
from src.models.meeting import MeetingModel
from src.schemas.meeting import MeetingCreate


class BaseMeetingRepository(ABC):
    @abstractmethod
    async def add(
        self, meeting_data: MeetingCreate, organizer_id: int
    ) -> MeetingModel: ...

    @abstractmethod
    async def get_by_id(self, meeting_id: int) -> MeetingModel | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[MeetingModel]: ...

    @abstractmethod
    async def get_user_meetings_in_time_range(
        self, user_id: int, start_time: datetime, end_time: datetime
    ) -> list[MeetingModel]: ...

    @abstractmethod
    async def delete(self, meeting: MeetingModel) -> None: ...


@dataclass
class SQLAlchemyMeetingRepository:
    _session: AsyncSession

    async def add(self, meeting_data: MeetingCreate, organizer_id: int) -> MeetingModel:
        meeting_model = MeetingModel(
            **meeting_data.model_dump(), organizer_id=organizer_id
        )
        self._session.add(meeting_model)
        await self._session.flush()
        await self._session.refresh(meeting_model)
        await self._session.commit()
        return meeting_model

    async def get_by_id(self, meeting_id: int) -> MeetingModel | None:
        stmt = (
            select(MeetingModel)
            .options(
                selectinload(MeetingModel.organizer),
                selectinload(MeetingModel.team),
            )
            .where(MeetingModel.id == meeting_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> list[MeetingModel]:
        stmt = (
            select(MeetingModel)
            .options(
                selectinload(MeetingModel.organizer),
                selectinload(MeetingModel.team),
            )
            .where(
                or_(
                    MeetingModel.organizer_id == user_id,
                    MeetingModel.participant_ids.any(user_id),
                )
            )
            .order_by(MeetingModel.start_time.asc())
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_user_meetings_in_time_range(
        self, user_id: int, start_time: datetime, end_time: datetime
    ) -> list[MeetingModel]:
        stmt = select(MeetingModel).where(
            and_(
                or_(
                    MeetingModel.organizer_id == user_id,
                    MeetingModel.participant_ids.any(user_id),
                ),
                or_(
                    and_(
                        MeetingModel.start_time <= start_time,
                        MeetingModel.end_time > start_time,
                    ),
                    and_(
                        MeetingModel.start_time < end_time,
                        MeetingModel.end_time >= end_time,
                    ),
                    and_(
                        MeetingModel.start_time >= start_time,
                        MeetingModel.end_time <= end_time,
                    ),
                ),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def delete(self, meeting: MeetingModel) -> None:
        await self._session.delete(meeting)
        await self._session.commit()
