from sqlalchemy import Column, DateTime, Integer, ForeignKey, CheckConstraint
from app.database import Base

class UserSymptom(Base):
    __tablename__ = "user_symptoms"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    symptom_id = Column(Integer, nullable=False)
    disease_id = Column(Integer, ForeignKey("diseases.id"), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    __table_args__ = (
        CheckConstraint(
            "(disease_id IS NULL) OR EXISTS (SELECT 1 FROM disease_symptom WHERE disease_symptom.disease_id = disease_id AND disease_symptom.symptom_id = symptom_id)",
            name="ck_us_valid_disease_symptom",
        ),
    )
