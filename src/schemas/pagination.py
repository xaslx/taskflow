from pydantic import BaseModel, Field, ConfigDict
from typing import Generic, TypeVar

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):

    items: list[T]
    total: int
    page: int
    size: int
    pages: int

    model_config = ConfigDict(from_attributes=True)


class PaginationParams(BaseModel):
    page: int = Field(ge=1, default=1)
    size: int = Field(ge=1, le=100, default=10)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size
