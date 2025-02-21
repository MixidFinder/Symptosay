from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.user_schema import UserRegister, UserResponse
from services.user_service import get_user_by_id, register_user, get_all_users

router = APIRouter()


@router.post("/auth", response_model=UserResponse)
async def authenticate_user(user: UserRegister, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_id(db, user.user_id)
    if db_user:
        return db_user
    return await register_user(db, user)


@router.get("/users", response_model=list[UserResponse])
async def list_all_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db)
    return [UserResponse.model_validate(user) for user in users]
