import hashlib

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def build_canonical(method: str, path: str, timestamp: str, body: bytes) -> str:
    
    # METHOD\nPATH\nTIMESTAMP\nSHA256(BODY)
    body_hash = sha256_hex(body)
    return "\n".join([method.upper(), path, timestamp, body_hash])