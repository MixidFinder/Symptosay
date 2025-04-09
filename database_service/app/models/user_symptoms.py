from sqlalchemy import Column, DateTime, Integer

from app.database import Base


class UserSymptom(Base):
    __tablename__ = "user_symptoms"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    symptom_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime)
