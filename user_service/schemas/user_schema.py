from __future__ import annotations

from pydantic import BaseModel


class UserRegister(BaseModel):
    user_id: int
    username: str
    is_admin: bool | None


class UserResponse(BaseModel):
    user_id: int
    username: str
    is_admin: bool


class UserListResponse(BaseModel):
    users: list[UserResponse]


class UserToggleAdmin(BaseModel):
    is_admin: bool
