from dataclasses import dataclass
from src.models.meeting import MeetingModel
from src.schemas.meeting import MeetingOut
from src.models.task import TaskModel
from src.repositories.meeting import BaseMeetingRepository
from src.repositories.task import BaseTaskRepository
from src.schemas.calendar import CalendarOut
from datetime import date as date_
from src.schemas.task import TaskOut





@dataclass
class DayCalendarUseCase:
    _task_repository: BaseTaskRepository
    _meeting_repository: BaseMeetingRepository

    async def execute(self, user_id: int, date: date_) -> CalendarOut:

        if not date:
            date: date_ = date_.today()

        tasks: list[TaskModel] = await self._task_repository.get_user_tasks_for_date(user_id=user_id, date=date)
        meetings: list[MeetingModel] = await self._meeting_repository.get_user_meetings_for_date(user_id=user_id, date=date)

        return CalendarOut(
            tasks=[TaskOut.model_validate(task) for task in tasks],
            meetings=[MeetingOut.model_validate(meeting) for meeting in meetings],
        )



@dataclass
class MonthCalendarUseCase:
    _task_repository: BaseTaskRepository
    _meeting_repository: BaseMeetingRepository

    async def execute(self, user_id: int, year: int, month: int) -> CalendarOut:

        if year is None or month is None:
            today = date_.today()
            year = year or today.year
            month = month or today.month

        tasks: list[TaskModel] = await self._task_repository.get_user_tasks_for_month(user_id=user_id, year=year, month=month)
        meetings: list[MeetingModel] = await self._meeting_repository.get_user_meetings_for_month(user_id=user_id, year=year, month=month)


        return CalendarOut(
            tasks=[TaskOut.model_validate(task) for task in tasks],
            meetings=[MeetingOut.model_validate(meeting) for meeting in meetings],
        )