### Mutual TLS (mTLS)

Both client and server present certificates to authenticate each other during the TLS handshake.
This ensures that both parties are verified, enhancing trust and security.
Successor to SSL
mTLS provides:
- Stronger authentication than one-way TLS.
- Encryption of data in transit.
- Protection against man-in-the-middle attacks.
- Mutual verification of identities.
- Granular access control based on client certificates.

Example usecases:
- k8 internal service communication
- Banking and Finteck APIs
- Service Mesh
- B2B transactions

### Implementing mTLS
#### Testing
TODO
