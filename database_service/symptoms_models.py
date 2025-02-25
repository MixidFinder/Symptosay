from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

# База для таблиц, связанных с симптомами:
SymptomsBase = declarative_base()

class Symptom(SymptomsBase):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Symptom(id={self.id}, name={self.name})>"
