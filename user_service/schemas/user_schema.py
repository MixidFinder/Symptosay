from datetime import datetime

from pydantic import BaseModel


class UserRegister(BaseModel):
    user_id: int
    username: str
    is_admin: bool


class UserResponse(UserRegister):
    is_blocked: bool
    created_date: datetime


class UserListResponse(BaseModel):
    users: list[UserResponse]


class UserToggleAdmin(BaseModel):
    is_admin: bool


class UserToggleBan(BaseModel):
    is_blocked: bool
