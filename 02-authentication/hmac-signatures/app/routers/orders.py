from fastapi import APIRouter, Depends
from app.security.hmac_auth import hmac_auth

router = APIRouter(prefix="/api/orders")

@router.post("")
async def create_order(payload: dict, _=Depends(hmac_auth)):
    return {"status": "order accepted", "payload": payload}