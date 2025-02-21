from sqlalchemy import Column, Integer, String, Boolean
from db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String)
    is_admin = Column(Boolean, default=False)
