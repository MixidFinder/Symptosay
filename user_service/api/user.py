import logging
from typing import Annotated

from db import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from models.user_model import User
from schemas.user_schema import UserRegister, UserResponse
from services.user_service import get_admins
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/api/users/register", response_model=UserResponse)
async def register_user(user: UserRegister, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    is_admin = user.user_id in get_admins()
    new_user = User(user_id=user.user_id, username=user.username, is_admin=is_admin)
    logger.info(f"Get new_user {new_user.user_id}, {new_user.username}, {new_user.is_admin}")

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"User {new_user.user_id}, {new_user.username} successfully registered")
    except Exception as e:
        logger.exception(f"Error registering user {user.user_id}: {e}")
        raise
    return new_user


@router.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> dict[str, str]:
    result = await db.execute(select(User).filter(User.user_id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/api/users", response_model=list[UserResponse])
async def list_all_users(db: Annotated[AsyncSession, Depends(get_db)]) -> list[UserResponse]:
    logger.info("Fetching all users from the database")
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        logger.info(f"Successfully fetched {len(users)} users")
    except Exception as e:
        logger.exception(f"Error fetching all users: {e}")
        raise
    return [UserResponse.model_validate(user) for user in users]
