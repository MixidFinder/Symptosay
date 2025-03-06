from pydantic import BaseModel
import datetime

class UserSymptomCreate(BaseModel):
    user_id: int
    symptom_id: int


class UserSymptomOut(BaseModel):
    id: int
    user_id: int
    symptom_id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True


class UserSymptomUpdate(BaseModel):
    new_symptom_id: int
