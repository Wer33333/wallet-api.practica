from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


# Схема для тела POST запроса — что принимаем от клиента
class OperationCreate(BaseModel):
    # pattern — регулярка, FastAPI автоматически вернёт 422 если придёт что-то другое
    operation_type: str = Field(..., pattern="^(DEPOSIT|WITHDRAW)$")
    # gt=0 — amount должен быть строго больше нуля
    amount: Decimal = Field(..., gt=0, decimal_places=2)


# Схема для ответа — что возвращаем клиенту
class WalletResponse(BaseModel):
    id: UUID
    balance: Decimal

    class Config:
        # from_attributes=True позволяет создать схему прямо из SQLAlchemy объекта
        from_attributes = True