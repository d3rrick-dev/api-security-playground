This section answers:
- How do services trust each other?
- How do we guarantee messages were not altered?
- How do we establish cryptographic identity, not just tokens?

### 1. Request Signing (Service-to-Service Trust)
- In service-to-service communication, request signing ensures that messages are authentic and unaltered.
- Zero-trust architectures often rely on request signing to verify the identity of services.
- Examples include AWS Signature Version 4 for API requests and signed webhooks from services like GitHub.

Differences from HMAC(Hash Based Message Authentication Code) Signatures:
- While HMAC(cryptographic primitive) signatures are typically used for client-to-server authentication, request signing is often employed in service-to-service contexts.
HMAC answers Given data and key -> produce a secure MAC.
- Request signing often includes additional metadata, such as canonical format, headers, timestamp, replay protection and key identification.

Replay Attack - 
Harmful in Financial or Irreversible Operations e.g reset pass, grant access
A replay is when a valid, previously captured request is sent again to trick a system into performing the same action twice.
Replay is not a security vulnerability by itself, it becomes a vulnerability when the operation is not replay-safe.
Https does not prevent replay attacks on its own, so request signing often includes timestamps and unique nonces to mitigate this risk.
e.g
- Replayed request
- Replayed token
- Replayed signature

How they happen:
- Compromised service logs
- Debug proxies (Burp, Charles)
- Leaked API gateway logs
- Insider threats
- Browser extensions
- Misconfigured reverse proxies

Preventing:
- Nonces (unique value per request i.e UUID, Rand(128-bit val)) to ensure each request is unique.
i.e `X-Nonce: 550e8400-e29b-41d4-a716-446655440000 & X-Signature: xyz789`, they are cached in the server side (Redis, Caffein, or DB with TTL) to track used nonces.
If changed signature will be invalid and reusing Nonce returns error.
- Idempotency keys to prevent duplicate processing(But more focused to business usecase)
- Request signing with timestamps to limit the validity period of a request.