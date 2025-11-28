from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class TaskBase(BaseModel):
    title: str
    description: str | None = Field(default=None)
    deadline: datetime | None = Field(default=None)


class TaskCreate(TaskBase):
    team_id: int
    status: TaskStatus = Field(default=TaskStatus.OPEN)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    status: TaskStatus | None = Field(default=None)
    deadline: datetime | None = Field(default=None) 
    assignee_id: int | None = Field(default=None) 


class TaskOut(TaskBase):
    
    id: int
    status: TaskStatus
    author_id: int
    team_id: int
    created_at: datetime
    updated_at: datetime
    comment: list['TaskCommentBase'] | None = Field(default=None)
    assignee_id: int | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)



class TaskCommentBase(BaseModel):
    text: str


class TaskCommentCreate(TaskCommentBase):
    ...

class TaskCommentOut(BaseModel):
    id: int
    author_id: int
    task_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)