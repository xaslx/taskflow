from dataclasses import dataclass
from src.repositories.meeting import BaseMeetingRepository
from src.schemas.meeting import MeetingOut
from src.models.meeting import MeetingModel


@dataclass
class GetUserMeetingsUseCase:
    _meeting_repository: BaseMeetingRepository

    async def execute(self, user_id: int) -> list[MeetingOut]:
        meetings: list[MeetingModel] = await self._meeting_repository.get_by_user_id(
            user_id
        )
        return [MeetingOut.model_validate(meeting) for meeting in meetings]
