import hmac, hashlib, json, datetime
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Request payload
BODY = json.dumps({"product": "laptop", "qty": 1}).encode()
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

CLIENT_ID = "demo-client"
KEY_ID = "key-2025-12"

# HKDF key derivation (must match backend)
MASTER = b"super-long-master-secret"
HKDF_KEY = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=CLIENT_ID.encode(),
    info=KEY_ID.encode()
).derive(MASTER)

# Canonical string
canonical = "\n".join([
    "POST",
    "/api/orders",
    TIMESTAMP,
    hashlib.sha256(BODY).hexdigest()
])

# HMAC signature
signature = hmac.new(HKDF_KEY, canonical.encode(), hashlib.sha256).hexdigest()

# Send request
import requests
headers = {
    "X-Client-Id": CLIENT_ID,
    "X-Key-Id": KEY_ID,
    "X-Timestamp": TIMESTAMP,
    "X-Signature": signature
}
resp = requests.post("http://127.0.0.1:8000/api/orders", headers=headers, data=BODY)
if resp.status_code != 200:
    print(resp.status_code, resp.text)
else:
    print(resp.status_code, resp.json())