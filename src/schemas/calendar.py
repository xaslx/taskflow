from src.schemas.task import TaskOut
from src.schemas.meeting import MeetingOut
from pydantic import BaseModel, ConfigDict


class CalendarOut(BaseModel):
    tasks: list[TaskOut]
    meetings: list[MeetingOut]


    model_config = ConfigDict(from_attributes=True)