from __future__ import annotations

from pydantic import BaseModel


class UserRegister(BaseModel):
    user_id: int
    username: str
    is_admin: bool | None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user_id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: list[UserResponse]

    class Config:
        from_attributes = True
