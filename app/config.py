from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Pydantic сам читает .env файл и подставляет переменные.
    # Если переменной нет в .env — используется значение по умолчанию.
    # postgresql+asyncpg:// — это асинхронный драйвер, требует пакет asyncpg
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db:5432/wallet_db"

    class Config:
        env_file = ".env"

# Создаём один экземпляр на всё приложение — импортируем его везде где нужен
settings = Settings()