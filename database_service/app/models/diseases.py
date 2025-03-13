from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, MetaData

DiseasesBase = declarative_base()
metadata_obj = MetaData()

disease_symptom = Table(
    "disease_symptom",
    metadata_obj,
    Column("disease_id", Integer, ForeignKey("diseases.id"), primary_key=True),
    Column("symptom_id", Integer, ForeignKey("symptoms.id"), primary_key=True),
)

class Disease(DiseasesBase):
    __tablename__ = "diseases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
