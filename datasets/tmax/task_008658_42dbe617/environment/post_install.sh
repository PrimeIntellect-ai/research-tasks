apt-get update && apt-get install -y python3 python3-pip openssl
    pip3 install pytest flask PyJWT requests cryptography

    mkdir -p /home/user/certs /home/user/server
    cd /home/user/certs

    # Generate main CA
    openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt -days 365 -nodes -subj "/CN=TargetCA" 2>/dev/null

    # Generate server_1.crt (Self-signed, invalid)
    openssl req -x509 -newkey rsa:2048 -keyout s1.key -out server_1.crt -days 365 -nodes -subj "/CN=Server1" 2>/dev/null

    # Generate server_2.crt (Valid, signed by TargetCA)
    openssl req -newkey rsa:2048 -keyout s2.key -out s2.csr -nodes -subj "/CN=Server2" 2>/dev/null
    openssl x509 -req -in s2.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server_2.crt -days 365 2>/dev/null

    # Generate server_3.crt (Signed by a different rogue CA, invalid)
    openssl req -x509 -newkey rsa:2048 -keyout rogue_ca.key -out rogue_ca.crt -days 365 -nodes -subj "/CN=RogueCA" 2>/dev/null
    openssl req -newkey rsa:2048 -keyout s3.key -out s3.csr -nodes -subj "/CN=Server3" 2>/dev/null
    openssl x509 -req -in s3.csr -CA rogue_ca.crt -CAkey rogue_ca.key -CAcreateserial -out server_3.crt -days 365 2>/dev/null

    cat << 'EOF' > /home/user/server/app.py
from flask import Flask, request, redirect, make_response
import jwt
import hashlib
import os

app = Flask(__name__)

def get_secret():
    cert_path = '/home/user/certs/server_2.crt'
    with open(cert_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

SECRET = get_secret()

@app.route('/login')
def login():
    redirect_uri = request.args.get('redirect')
    token = request.args.get('token')

    if not redirect_uri or not token:
        return "Missing parameters", 400

    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        if decoded.get('redirect') != redirect_uri or decoded.get('user') != 'admin':
            return "Invalid payload", 403

        resp = make_response(redirect(redirect_uri, code=302))
        resp.set_cookie('SessionAuth', 'red-team-success-cookie-val', httponly=True)
        return resp
    except Exception as e:
        return "Invalid token", 403

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user