from fastapi import FastAPI
from app.routers import orders

app = FastAPI(title="HMAC API Demo")

app.include_router(orders.router)