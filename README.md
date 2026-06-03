# Wallet API
REST API для управления балансами пользовательских кошельков.

## Стек

- Python 3.12
- FastAPI 
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker + docker-compose
- pytest

# запуск

```bash
docker-compose up --build
```

API будет доступен на `http://localhost:8000`

Документация: `http://localhost:8000/docs`

## Эндпоинты

### Получить баланс кошелька
```
GET /api/v1/wallets/{wallet_id}
```

### Пополнение или списание
```
POST /api/v1/wallets/{wallet_id}/operation
```

Тело запроса:
```json
{
  "operation_type": "DEPOSIT",
  "amount": 1000
}
```

`operation_type` — `DEPOSIT` (пополнение) или `WITHDRAW` (списание)

## Тесты

```bash
venv/bin/pytest tests/ -v
```

## Особенности реализации

- Конкурентные запросы к одному кошельку обрабатываются корректно через `SELECT FOR UPDATE`
- Баланс хранится как `NUMERIC(20,2)` — без погрешностей float
- Миграции через Alembic
