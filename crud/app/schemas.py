from typing import Optional

from pydantic import BaseModel


class BookIn(BaseModel):
    title: str
    description: Optional[str] = None


class BookInDBBase(BookIn):
    id: int

    class Config:
        from_attributes = True
