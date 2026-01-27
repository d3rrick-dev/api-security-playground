from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from enum import Enum
from datetime import datetime, timedelta

class KeyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    GRACE = "GRACE"
    REVOKED = "REVOKED"

# Master secrets per client
MASTER_SECRETS = {
    "demo-client": b"super-long-master-secret"
}

# Key metadata (rotation)
KEY_STORE = {
    "demo-client": {
        "key-2026-01": {
            "status": KeyStatus.ACTIVE,
            "expires_at": datetime.now() + timedelta(days=30)
        },
        "key-2025-12": {
            "status": KeyStatus.GRACE,
            "expires_at": datetime.now() + timedelta(days=7)
        }
    }
}

def derive_hmac_key(client_id: str, key_id: str) -> bytes:
    """Derive a per-key HMAC key using HKDF"""
    master = MASTER_SECRETS.get(client_id)
    if not master:
        raise ValueError("Unknown client")
    info = key_id.encode()
    salt = client_id.encode()
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info
    )
    return hkdf.derive(master)

def get_key_status(client_id: str, key_id: str):
    try:
        return KEY_STORE[client_id][key_id]["status"]
    except KeyError:
        raise ValueError("Invalid client/key")