from typing import Optional

from pydantic import BaseModel, Field


class SymptomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class SymptomOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class SymptomsBatchCreate(BaseModel):
    names: list[str]
