
# HMAC Authentication Demo

## Features
- HMAC-SHA256 request signing
- Canonical request format
- HKDF-derived keys for rotation
- Replay protection (timestamps & signature uniqueness)

Practical usecases of HMAC
1. API Request Signing
- Client computes HMAC of request (canonicalized) using shared key. Server validates HMAC.
- AWS Signature for API requests

2. Webhook Verification
- Third-party service sends payload + HMAC signature. Receiver validates.
- Stripe, GitHub webhooks

3. Session Tokens / Cookies
- Sign session data to detect tampering.
- Django signed_cookie, Flask itsdangerous

4. File Integrity Verification
- Compute HMAC for large files to detect tampering.
- Software distribution (update servers)

5. Internal Microservices Auth
- Services share secret and validate each other’s requests.
- Payment processing between internal APIs

## Usage
1. Start backend:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000

# run client demo
python client/sign_request.py

#Response
200 {'status': 'order accepted', 'payload': {'product': 'laptop', 'qty': 1}}
```




