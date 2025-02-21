import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import User
from schemas.user_schema import UserRegister

logger = logging.getLogger(__name__)


async def register_user(db: AsyncSession, user: UserRegister):
    new_user = User(user_id=user.user_id, username=user.username, is_admin=False)
    logger.info(f"Get new_user {new_user.user_id}, {new_user.username}")
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(
            f"User {new_user.user_id}, {new_user.username} successfully registered"
        )
    except Exception as e:
        logger.error(f"Error registering user {user.user_id}: {e}")
    return new_user


async def get_all_users(db: AsyncSession):
    logger.info("Fetching all users from the database")
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        logger.info(f"Successfully fetched {len(users)} users")
    except Exception as e:
        logger.error(f"Error fetching all users: {e}")
        raise

    return users


async def get_user_by_id(db: AsyncSession, user_id: int):
    logger.info(f"Fetching user by ID: {user_id}")

    try:
        result = await db.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if user:
            logger.info(f"User found: {user.username} (ID: {user.user_id})")
        else:
            logger.warning(f"No user found with ID: {user_id}")
    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {e}")
        raise

    return user
