from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime

UserSymptomsBase = declarative_base()

class UserSymptom(UserSymptomsBase):
    __tablename__ = "user_symptoms"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    symptom_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime)
