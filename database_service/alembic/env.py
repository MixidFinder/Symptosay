import asyncio
import os
from logging.config import fileConfig

from dotenv import load_dotenv
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

# 1) Подгружаем переменные окружения из файла .env
load_dotenv()

# Из окружения берём ссылки на три разные базы (если действительно три отдельных БД)
USERS_DB_URL = os.getenv("USERS_DATABASE_URL")
SYMPTOMS_DB_URL = os.getenv("SYMPTOMS_DATABASE_URL")
USER_SYMPTOMS_DB_URL = os.getenv("USER_SYMPTOMS_DATABASE_URL")

# 2) Получаем объект конфигурации Alembic
config = context.config

# 3) Настраиваем логгирование, если указан конфигурационный файл
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4) В зависимости от того, какой .ini запущен,
#    выбираем соответствующую базу и набор моделей
filename = config.config_file_name or ""

if "alembic_symptoms.ini" in filename.lower():
    if not SYMPTOMS_DB_URL:
        raise ValueError("SYMPTOMS_DATABASE_URL не установлена в окружении (.env), а вы запускаете alembic_symptoms.ini")

    config.set_main_option("SYMPTOMS_DATABASE_URL", SYMPTOMS_DB_URL)
    from symptoms_models import SymptomsBase
    import symptoms_models  # Важно, чтобы модели были импортированы

    Base = SymptomsBase

elif "alembic_users.ini" in filename.lower():
    if not USERS_DB_URL:
        raise ValueError("USERS_DATABASE_URL не установлена в окружении (.env), а вы запускаете alembic_users.ini")

    config.set_main_option("USERS_DATABASE_URL", USERS_DB_URL)
    from user_models import UsersBase
    import user_models

    Base = UsersBase

elif "alembic_user_symptoms.ini" in filename.lower():
    if not USER_SYMPTOMS_DB_URL:
        raise ValueError("USER_SYMPTOMS_DATABASE_URL не установлена в окружении (.env), а вы запускаете alembic_user_symptoms.ini")

    config.set_main_option("USER_SYMPTOMS_DATABASE_URL", USER_SYMPTOMS_DB_URL)
    from user_symptoms_models import UserSymptomsBase
    import user_symptoms_models

    Base = UserSymptomsBase

else:
    raise ValueError(
        "Не могу определить, для какой базы запускать миграции. "
        "Проверьте, что -c указывает на alembic_symptoms.ini / alembic_users.ini / alembic_user_symptoms.ini"
    )

target_metadata = Base.metadata

# -----------------------------
# Ниже — стандартные функции Alembic
# -----------------------------

def run_migrations_offline() -> None:
    """
    Выполнение миграций в offline-режиме (без реального подключения к БД).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """
    Выполнение миграций в online-режиме с использованием асинхронного движка.
    """
    DATABASE_URL = config.get_main_option("sqlalchemy.url")

    async_engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        poolclass=pool.NullPool,
    )

    async with async_engine.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=target_metadata
            )
        )
        async with connection.begin():
            await connection.run_sync(lambda conn: context.run_migrations())

    await async_engine.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
