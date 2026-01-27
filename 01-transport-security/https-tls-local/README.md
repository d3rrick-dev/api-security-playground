## Simple https service

## 1. Simple TLS
### Installations
- N.B I'm using a mac
```bash
brew install mkcert

# creates a local certificate authority (CA)
# Adds to local OS trust store
# Allows browser $ curl to trust your certs
mkcert -install

# You'll get this success message
# The local CA is now installed in the system trust store!
```

### Create https folder
```bash
mkdir -p 01-transport-security/https-tls-local/certs
cd 01-transport-security/https-tls-local


mkcert \
  -key-file certs/server-key.pem \
  -cert-file certs/server.pem \
  localhost 127.0.0.1 ::1

  ## you'll have server-key.pem server.pem files
```

### Running server
```bash
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8443 \
  --ssl-keyfile certs/server-key.pem \
  --ssl-certfile certs/server.pem
```

### Testing
```bash 
# Successful
curl https://localhost:8443/health

# Fails — no HTTP listener
http://localhost:8443/health

#Confirming TLS
openssl s_client -connect localhost:8443
#N.B since mkcert is for testing purposes, there will still be some trust warnings (there are work arounds like asking Openssl to trust mkcert CA or ignore - local or testing)
```

## 2. Adding SSL Termination
i.e a point where HTTPS traffic is decrypted(terminated) before reaching backend server.

- Traffic from the client → encrypted via TLS (HTTPS)
- SSL termination → decrypts it
- Backend → receives plain HTTP traffic


N.B 
- Backend listens on HTTP only (port 8000).
- SSL termination will happen at the reverse proxy.

### Running the app
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Running nginx (Executing on the same working directory)
```bash
docker run -d -p 8443:8443 \
    -v $(pwd)/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro \
    -v $(pwd)/certs:/etc/nginx/certs:ro \
    nginx:latest
```

### Testing
```bash
curl -k https://localhost:8443/health
# {"status": "backend running"}
```