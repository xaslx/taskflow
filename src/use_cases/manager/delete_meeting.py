from dataclasses import dataclass
from src.models.meeting import MeetingModel
from src.repositories.meeting import BaseMeetingRepository
from src.exceptions.meeting import MeetingNotFoundException
from src.exceptions.user import ForbiddenException


@dataclass
class DeleteMeetingUseCase:
    _meeting_repository: BaseMeetingRepository

    async def execute(self, meeting_id: int, user_id: int, user_team_id: int) -> None:

        meeting: MeetingModel | None = await self._meeting_repository.get_by_id(
            meeting_id
        )

        if not meeting:
            raise MeetingNotFoundException()

        if meeting.team_id != user_team_id:
            raise ForbiddenException()

        if meeting.organizer_id != user_id:
            raise ForbiddenException()

        await self._meeting_repository.delete(meeting)
