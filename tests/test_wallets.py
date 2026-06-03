import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Wallet
from decimal import Decimal

async def create_wallet(db: AsyncSession, balance: float = 1000.00) -> Wallet:
    wallet = Wallet(balance = Decimal(str(balance)))
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return wallet

@pytest.mark.asyncio
async def test_get_wallet_success(client: AsyncClient, db_session: AsyncSession):
    wallet = await create_wallet(db_session, balance= 500.00)
    response = await client.get(f"/api/v1/wallets/{wallet.id}")
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 500.00

@pytest.mark.asyncio
async def test_get_wallet_not_found(client: AsyncClient):
    response = await client.get("/api/v1/wallets/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
                             
@pytest.mark.asyncio
async def test_deposit_success(client: AsyncClient, db_session: AsyncSession):
    wallet = await create_wallet(db_session, balance=1000.00)

    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json = {"operation_type": "DEPOSIT", "amount": 500}
    )

    assert response.status_code == 200
    assert float(response.json()["balance"]) == 1500.00

@pytest.mark.asyncio
async def test_withdraw_succsess(client: AsyncClient, db_session: AsyncClient):
    wallet = await create_wallet(db_session, balance = 1000.00)
    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json = {"operation_type": "WITHDRAW", "amount": 300}
    )
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 700.00

@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(client: AsyncClient, db_session: AsyncSession):
    wallet = await create_wallet(db_session,balance = 100.00)
    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json = {"operation_type": "WITHDRAW", "amount": 999}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_invalid_operation_type(client: AsyncClient, db_session: AsyncSession):
    wallet = await create_wallet(db_session, balance = 100.00)
    response = await client.post(
        f"/api/v1/wallets/{wallet.id}/operation",
        json = {"operation_type": "INVALID", "amount": 50}
    )
    assert response.status_code == 422