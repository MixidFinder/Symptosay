from typing import Optional
import datetime
from pydantic import BaseModel, Field

class UserSymptomCreate(BaseModel):
    user_id: int
    symptom_id: int
    disease_id: Optional[int] = Field(default=None)

class UserSymptomOut(BaseModel):
    id: int
    user_id: int
    symptom_id: int
    disease_id: Optional[int] = None
    timestamp: datetime.datetime
    class Config:
        from_attributes = True

class UserSymptomUpdate(BaseModel):
    new_symptom_id: int
    new_disease_id: Optional[int] = None
