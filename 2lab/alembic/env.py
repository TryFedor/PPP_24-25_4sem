from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Импортируем Base и модели из твоего проекта
from app.db import Base  # Метаданные SQLAlchemy
from app.models.user import User  # Пример импорта модели
# Добавь другие модели, если они есть (например, Post, Comment и т.д.)

# Этот импорт важен для того, чтобы Alembic видел все модели
# и мог отслеживать изменения в схеме БД.

# -------------------------------
# Основные настройки Alembic
# -------------------------------
config = context.config

# Если ты используешь .env для настроек БД,
# замени sqlalchemy.url на значение из config:
# from app.core.config import settings
# config.set_main_option("sqlalchemy.url", settings.DB_URL)

# Подключаем логирование (можно оставить как есть)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные SQLAlchemy (Base)
target_metadata = Base.metadata

# -------------------------------
# Функции для запуска миграций
# -------------------------------
def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Запуск миграций в online-режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

# -------------------------------
# Запуск миграций
# -------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
