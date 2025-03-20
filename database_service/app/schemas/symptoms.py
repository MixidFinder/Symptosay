from typing import Optional

from pydantic import BaseModel


class SymptomCreate(BaseModel):
    name: str
    description: Optional[str] = None


class SymptomOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class SymptomsBatchCreate(BaseModel):
    names: str
