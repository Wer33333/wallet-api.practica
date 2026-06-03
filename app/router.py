from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Wallet
from app.schemas import OperationCreate, WalletResponse

router = APIRouter(prefix="/api/v1/wallets", tags=["wallets"])


@router.post("/{wallet_id}/operation", response_model=WalletResponse)
async def wallet_operation(
    wallet_id: UUID,
    op: OperationCreate,
    db: AsyncSession = Depends(get_db),  # FastAPI сам вызовет get_db и передаст сессию
):
    # WITH FOR UPDATE — блокирует строку в БД до конца транзакции.
    # Если два запроса пришли одновременно к одному кошельку —
    # второй будет ждать пока первый не сделает commit.
    # Без этого оба прочитают баланс 100, оба спишут 50, оба запишут 50 — вместо 0.
    result = await db.execute(
        select(Wallet).where(Wallet.id == wallet_id).with_for_update()
    )
    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if op.operation_type == "WITHDRAW":
        if wallet.balance < op.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        wallet.balance -= op.amount
    else:
        wallet.balance += op.amount

    # commit() сохраняет изменения в БД и снимает блокировку WITH FOR UPDATE
    await db.commit()
    await db.refresh(wallet)  # обновляем объект из БД чтобы вернуть актуальные данные
    return wallet


@router.get("/{wallet_id}", response_model=WalletResponse)
async def get_wallet(
    wallet_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Wallet).where(Wallet.id == wallet_id)
    )
    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return wallet