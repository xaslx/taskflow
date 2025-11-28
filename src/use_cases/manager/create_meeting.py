from dataclasses import dataclass
from src.exceptions.meeting import TimeConflictException
from src.models.user import UserModel
from src.repositories.meeting import BaseMeetingRepository
from src.repositories.user import BaseUserRepository
from src.repositories.team import BaseTeamRepository
from src.schemas.meeting import MeetingCreate, MeetingOut
from src.exceptions.user import UserNotInTeamException
from src.models.meeting import MeetingModel


@dataclass
class CreateMeetingUseCase:
    _meeting_repository: BaseMeetingRepository
    _user_repository: BaseUserRepository
    _team_repository: BaseTeamRepository

    async def execute(self, meeting_data: MeetingCreate, organizer_id: int) -> MeetingOut:

        organizer: UserModel | None = await self._user_repository.get_by_id(organizer_id)

        if not organizer or organizer.team_id != meeting_data.team_id:
            raise UserNotInTeamException()
        

        for user_id in meeting_data.participant_ids:

            user: UserModel | None = await self._user_repository.get_by_id(user_id)

            if not user or user.team_id != meeting_data.team_id:
                raise UserNotInTeamException()

        for user_id in meeting_data.participant_ids:

            user: UserModel | None = await self._user_repository.get_by_id(user_id)
            
            if not user or user.team_id != meeting_data.team_id:
                raise UserNotInTeamException()
        

        for user_id in meeting_data.participant_ids + [organizer_id]:

            conflicting_meetings: MeetingModel | None = await self._meeting_repository.get_user_meetings_in_time_range(
                user_id, 
                meeting_data.start_time, 
                meeting_data.end_time
            )
            
            if conflicting_meetings:
                raise TimeConflictException()
        
  
        meeting: MeetingModel = await self._meeting_repository.add(meeting_data, organizer_id)
        return MeetingOut.model_validate(meeting)