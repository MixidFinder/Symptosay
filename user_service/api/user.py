import logging
from typing import Annotated

from db import get_db
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from models.user_model import User
from pydantic import ValidationError
from schemas.user_schema import UserRegister, UserResponse, UserToggleAdmin, UserToggleBan
from services.user_service import get_admins
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

logger = logging.getLogger(__name__)


# TODO: change to put
@router.post("/api/users/register")
async def register_user(user: UserRegister, db: Annotated[AsyncSession, Depends(get_db)]) -> dict[str, str]:
    is_admin = user.user_id in get_admins()
    new_user = User(user_id=user.user_id, username=user.username, is_admin=is_admin)
    logger.info("Get new_user %s, %s, %s", new_user.user_id, new_user.username, new_user.is_admin)
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info("User %s, %s successfully registered", new_user.user_id, new_user.username)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation Error") from e

    return {"detail": "User registered"}


@router.get("/api/users/{user_id}")
async def get_user_by_id(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    logger.info("Searching for user with ID %s", user_id)
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/api/users/{username}")
async def get_user_by_username(username: str, db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    logger.info("Searching for user with username: %s", username)
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/api/users")
async def list_all_users(db: Annotated[AsyncSession, Depends(get_db)]) -> list[UserResponse]:
    logger.info("Fetching all users from the database")
    result = await db.execute(select(User))
    users = result.scalars().all()
    return list(users)


@router.patch("/api/users/{username}/toggle-admin")
async def toggle_admin(data: UserToggleAdmin, db: Annotated[AsyncSession, Depends(get_db)]) -> dict[str, str]:
    logger.info("Toggle is_admin for user: %s to %s", data.username, data.is_admin)
    result = await db.execute(select(User).where(User.username == data.username))

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_admin = data.is_admin
    await db.commit()
    await db.refresh(user)

    if user.is_admin is True:
        return {"detail": "User promoted to admin"}

    if user.is_admin is False:
        return {"detail": "User demoted"}

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")


@router.patch("/api/users/{user_id}/toggle-ban")
async def toggle_ban(user_id: int, data: UserToggleBan, db: Annotated[AsyncSession, Depends(get_db)]) -> dict[str, str]:
    logger.info("Toggle ban for user: %s, to %s", user_id, data.is_blocked)
    user = await db.get(User, user_id)
    logger.info("Get user: %s", user)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_blocked = data.is_blocked
    await db.commit()
    await db.refresh(user)

    if user.is_blocked is True:
        return {"detail": "User is blocked"}

    if user.is_blocked is False:
        return {"detail": "User is unblocked"}

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")
