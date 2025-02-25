from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

# База для таблиц, связанных с пользователями:
UsersBase = declarative_base()

class User(UsersBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
