import uuid
from decimal import Decimal
from sqlalchemy import Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


# DeclarativeBase — это базовый класс от которого наследуются все модели.
# Alembic смотрит на Base.metadata чтобы понять какие таблицы существуют.
class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = "wallets"

    # UUID как первичный ключ — стандарт для публичных API.
    # default=uuid.uuid4 означает что Python сам генерирует id при создании объекта.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Numeric(20, 2) — число до 20 знаков, из них 2 после запятой.
    # Никогда не float для денег — float даёт погрешности при арифметике.
    balance: Mapped[Decimal] = mapped_column(
        Numeric(20, 2),
        nullable=False,
        default=Decimal("0.00"),
    )