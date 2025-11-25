from pydantic import BaseModel, ConfigDict




class CreateTeamSchema(BaseModel):
    name: str


class TeamOut(BaseModel):
    id: int
    name: str
    code: str
    users: list['UserOut']

    model_config = ConfigDict(from_attributes=True)
