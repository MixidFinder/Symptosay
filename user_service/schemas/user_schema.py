from typing import List, Optional
from pydantic import BaseModel


class UserRegister(BaseModel):
    user_id: int
    username: str
    is_admin: Optional[bool] = False

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user_id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: List[UserResponse]

    class Config:
        from_attributes = True
