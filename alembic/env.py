import asyncio
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# Импортируем Base чтобы Alembic знал о структуре таблиц
# Импорт Wallet обязателен — без него Alembic не увидит модель даже если Base импортирован
from app.models import Base, Wallet  # noqa: F401
from app.config import settings

config = context.config
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    # Offline режим — миграции генерируются как SQL файл без подключения к БД
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    # Online режим — подключается к реальной БД и применяет миграции
    # URL берём из settings а не из alembic.ini — один источник правды
    connectable = create_async_engine(settings.DATABASE_URL)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()  # закрываем соединение после миграций


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())