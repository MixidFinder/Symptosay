import datetime
from typing import Optional

from pydantic import BaseModel


class UserSymptomCreate(BaseModel):
    user_id: int
    symptom_id: int
    disease_id: Optional[int] = None


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


class UserSymptomOutStr(BaseModel):
    user_id: int
    symptom_name: str
    disease_name: str
    timestamp: datetime.datetime
