from pydantic import BaseModel, ConfigDict, Field
from src.schemas.user import UserOut


class CreateTeamSchema(BaseModel):
    name: str = Field(max_length=50)


class JoinTeam(BaseModel):
    code: str


class TeamOut(BaseModel):
    id: int
    name: str
    code: str
    model_config = ConfigDict(from_attributes=True)


class AddMember(BaseModel):
    user_id: int


class TeamOutWithUsers(TeamOut):
    users: list[UserOut]
