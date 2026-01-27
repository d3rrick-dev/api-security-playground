from datetime import datetime, timedelta

USED_SIGNATURES = set()
MAX_SKEW = timedelta(minutes=5)

def validate_replay(timestamp: str, signature: str):
    # Convert ISO timestamp
    request_time = datetime.fromisoformat(timestamp.replace("Z", ""))
    now = datetime.utcnow()

    if abs(now - request_time) > MAX_SKEW:
        raise ValueError("Request expired")

    if signature in USED_SIGNATURES:
        raise ValueError("Replay detected")

    USED_SIGNATURES.add(signature)