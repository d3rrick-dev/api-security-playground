import hmac
import hashlib
from fastapi import Header, Request, HTTPException,status
from app.security.canonical import build_canonical
from app.security.key_store import derive_hmac_key, get_key_status, KeyStatus
from app.security.replay_protection import validate_replay

async def hmac_auth(
    request: Request,
    x_client_id: str = Header(...),
    x_key_id: str = Header(...),
    x_timestamp: str = Header(...),
    x_signature: str = Header(...)
):
    # Check key status
    status = get_key_status(x_client_id, x_key_id)
    if status == KeyStatus.REVOKED:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Revoked key")

    # Read body
    body = await request.body()

    # Canonical string
    canonical = build_canonical(
        request.method,
        request.url.path,
        x_timestamp,
        body
    )

    # Derive HMAC key
    key = derive_hmac_key(x_client_id, x_key_id)
    expected = hmac.new(key, canonical.encode(), hashlib.sha256).hexdigest()

    # Replay protection
    try:
        validate_replay(x_timestamp, x_signature)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    # Constant-time compare
    if not hmac.compare_digest(expected, x_signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")