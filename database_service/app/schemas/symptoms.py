from pydantic import BaseModel
from typing import Optional

class SymptomCreate(BaseModel):
    name: str
    description: Optional[str] = None


class SymptomOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class SymptomsBatchCreate(BaseModel):
    names: str
