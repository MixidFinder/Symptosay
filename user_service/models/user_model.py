from db import Base
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True)
    username: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
