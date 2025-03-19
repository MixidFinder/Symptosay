from pydantic import BaseModel
from typing import Optional

class DiseaseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class DiseaseOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True
