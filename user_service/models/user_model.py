from db import Base
from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String)
    is_admin = Column(Boolean, default=False)
