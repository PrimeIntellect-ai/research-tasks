apt-get update && apt-get install -y python3 python3-pip openssl make
pip3 install pytest fastapi uvicorn pyjwt

mkdir -p /app/vendored/jwt-auth-svc-1.2.0/certs
mkdir -p /app/vendored/jwt-auth-svc-1.2.0/app

cd /app/vendored/jwt-auth-svc-1.2.0/certs

# Generate CA
openssl genrsa -out root.key 2048
openssl req -x509 -new -nodes -key root.key -sha256 -days 3650 -out root.pem -subj "/C=US/ST=State/L=City/O=Org/CN=RootCA"

# Generate Intermediate
openssl genrsa -out intermediate.key 2048
openssl req -new -key intermediate.key -out intermediate.csr -subj "/C=US/ST=State/L=City/O=Org/CN=IntermediateCA"
openssl x509 -req -in intermediate.csr -CA root.pem -CAkey root.key -CAcreateserial -out intermediate.crt -days 3650 -sha256

# Generate Server
openssl genrsa -out server_unencrypted.key 2048
openssl req -new -key server_unencrypted.key -out server.csr -subj "/C=US/ST=State/L=City/O=Org/CN=127.0.0.1"
openssl x509 -req -in server.csr -CA intermediate.crt -CAkey intermediate.key -CAcreateserial -out server.crt -days 3650 -sha256

# Encrypt Server key
openssl rsa -aes128 -passout pass:4829 -in server_unencrypted.key -out server.key

rm -f server_unencrypted.key root.key intermediate.key intermediate.csr server.csr root.srl intermediate.srl

cd /app/vendored/jwt-auth-svc-1.2.0

cat << 'EOF' > Makefile
run:
	pythn3 -m app.main
EOF

cat << 'EOF' > app/__init__.py
EOF

cat << 'EOF' > app/auth.py
import jwt

def verify_token(token, secret):
    return jwt.decode(token, secret, algorithms=["HS256", "none"])
EOF

cat << 'EOF' > app/main.py
import os
import uvicorn
import asyncio
from fastapi import FastAPI, Header, HTTPException
from app.auth import verify_token

app = FastAPI()
JWT_SECRET = os.environ.get("JWT_SECRET")

@app.get("/api/secure")
def secure_endpoint(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.replace("Bearer ", "")
    try:
        payload = verify_token(token, JWT_SECRET)
        return {"status": "ok", "payload": payload}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

async def run_servers():
    if not JWT_SECRET:
        import sys
        sys.exit(1)

    pwd = None
    if os.path.exists("/home/user/key_password.txt"):
        with open("/home/user/key_password.txt", "r") as f:
            pwd = f.read().strip()

    config_http = uvicorn.Config(app, host="127.0.0.1", port=8080)
    server_http = uvicorn.Server(config_http)

    config_https = uvicorn.Config(app, host="127.0.0.1", port=8443, 
                                  ssl_certfile="certs/fullchain.pem", 
                                  ssl_keyfile="certs/server.key",
                                  ssl_keyfile_password=pwd)
    server_https = uvicorn.Server(config_https)

    await asyncio.gather(server_http.serve(), server_https.serve())

if __name__ == "__main__":
    asyncio.run(run_servers())
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app