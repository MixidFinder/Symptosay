from pydantic import BaseModel, Field
from typing import Optional, List

from pydantic import BaseModel


class SymptomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class SymptomOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class SymptomsBatchCreate(BaseModel):
    names: List[str]

