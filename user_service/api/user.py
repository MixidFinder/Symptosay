import logging
from collections.abc import Sequence
from typing import Annotated

from db import get_db
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from models.user_model import User
from schemas.user_schema import UserRegister, UserResponse, UserToggleAdmin
from services.user_service import get_admins
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/api/users/register")
async def register_user(user: UserRegister, db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    is_admin = user.user_id in get_admins()
    new_user = User(user_id=user.user_id, username=user.username, is_admin=is_admin)
    logger.info("Get new_user %s, %s, %s", new_user.user_id, new_user.username, new_user.is_admin)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logger.info("User %s, %s successfully registered", new_user.user_id, new_user.username)

    return new_user


@router.get("/api/users/{user_id}")
async def get_user_by_id(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    logger.info("Searching for user with ID %s", user_id)
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/api/users")
async def list_all_users(db: Annotated[AsyncSession, Depends(get_db)]) -> Sequence[User]:
    logger.info("Fetching all users from the database")
    result = await db.execute(select(User))
    return result.scalars().all()


@router.patch("/api/users/{user_id}/toggle-admin")
async def toggle_admin(
    user_id: int, data: UserToggleAdmin, db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    logger.info("Promoting to admin user %s", user_id)
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_admin = data.is_admin
    await db.commit()
    await db.refresh(user)

    return user
