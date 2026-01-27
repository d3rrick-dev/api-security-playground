## Simple https service

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