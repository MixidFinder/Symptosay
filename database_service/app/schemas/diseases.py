from typing import Optional

from pydantic import BaseModel


class DiseaseCreate(BaseModel):
    name: str
    description: Optional[str] = None


class DiseaseOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
