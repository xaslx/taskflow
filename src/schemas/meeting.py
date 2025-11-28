from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime



class MeetingBase(BaseModel):
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)
    start_time: datetime
    end_time: datetime
    participant_ids: list[int] = Field(default=[])

    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, end_time: datetime, info):
        start_time = info.data.get('start_time')
        if start_time and end_time <= start_time:
            raise ValueError('Время окончания должно быть после времени начала')
        return end_time



class MeetingCreate(MeetingBase):
    team_id: int


class MeetingUpdate(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)
    participant_ids: list[int] | None = Field(default=None)


class MeetingOut(MeetingBase):
    id: int
    organizer_id: int
    team_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)