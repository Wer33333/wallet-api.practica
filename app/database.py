from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings
from app.models import Base


# Engine — это соединение с БД. echo=True печатает SQL в консоль, удобно при разработке.
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Фабрика сессий. Сессия — это единица работы с БД (один запрос или транзакция).
# expire_on_commit=False — объекты не сбрасываются после commit, можно читать поля дальше.
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# Эта функция — dependency для FastAPI (используется через Depends).
# Она создаёт сессию на время одного HTTP запроса и закрывает после.
# AsyncGenerator означает что функция отдаёт значение (yield) и потом продолжает (закрывает сессию).
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session