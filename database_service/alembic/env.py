import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()

SYMPTOMS_DB_URL = os.getenv("SYMPTOMS_DATABASE_URL")
USER_SYMPTOMS_DB_URL = os.getenv("USER_SYMPTOMS_DATABASE_URL")

filename = context.config.config_file_name.lower() if context.config else ""

if "alembic_symptoms.ini" in filename:
    if not SYMPTOMS_DB_URL:
        raise ValueError(
            "SYMPTOMS_DATABASE_URL не установлена в окружении (.env), "
            "а вы запускаете alembic_symptoms.ini"
        )
    context.config.set_main_option("sqlalchemy.url", SYMPTOMS_DB_URL)

elif "alembic_user_symptoms.ini" in filename:
    if not USER_SYMPTOMS_DB_URL:
        raise ValueError(
            "USER_SYMPTOMS_DATABASE_URL не установлена в окружении (.env), "
            "а вы запускаете alembic_user_symptoms.ini"
        )
    context.config.set_main_option("sqlalchemy.url", USER_SYMPTOMS_DB_URL)
else:
    raise ValueError(
        "Не могу определить, для какой базы запускать миграции. Проверьте, что -c "
        "указывает на alembic_symptoms.ini или alembic_user_symptoms.ini"
    )

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models.symptoms import SymptomsBase

from app.models.user_symptoms import UserSymptomsBase

target_metadata = None

if "alembic_symptoms.ini" in filename:
    target_metadata = SymptomsBase.metadata
elif "alembic_user_symptoms.ini" in filename:
    target_metadata = UserSymptomsBase.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),  
        prefix="sqlalchemy.",  
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,  
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
