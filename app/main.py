from fastapi import FastAPI
from app.router import router

app = FastAPI(title = "Wallet API")
app.include_router(router)