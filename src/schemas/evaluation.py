from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime



class EvaluationBase(BaseModel):
    score: int = Field(ge=1, le=5)

class EvaluationCreate(EvaluationBase):
    task_id: int


class EvaluationOut(EvaluationBase):
    
    id: int
    task_id: int
    user_id: int
    evaluator_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
