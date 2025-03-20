from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.database import Base


class DiseaseSymptom(Base):
    __tablename__ = "disease_symptom"

    disease_id = Column(Integer, ForeignKey("diseases.id"), primary_key=True)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), primary_key=True)


class Disease(Base):
    __tablename__ = "diseases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
