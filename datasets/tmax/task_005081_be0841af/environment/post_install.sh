apt-get update && apt-get install -y python3 python3-pip curl nginx gcc binutils
    pip3 install pytest flask pyjwt

    mkdir -p /app/bin /app/corpus/clean /app/corpus/evil

    # Create audit.py
    cat << 'EOF' > /app/audit.py
from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/api/audit/health')
def health():
    return jsonify({"status": "ok"})
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082)
EOF

    # Create auth_svc binary
    cat << 'EOF' > /app/auth_svc.c
#include <stdio.h>
#include <unistd.h>
int main() {
    const char* secret = "SUP3R_S3CR3T_HMAC_K3Y_9912";
    while(1) { sleep(100); }
    return 0;
}
EOF
    gcc /app/auth_svc.c -o /app/bin/auth_svc
    rm /app/auth_svc.c

    # Create nginx.conf
    cat << 'EOF' > /app/nginx.conf
events {}
http {
    server {
        listen 8080;
        # location /api/auth { proxy_pass http://127.0.0.1:8081; }
        # location /api/audit { proxy_pass http://127.0.0.1:8082; }
    }
}
EOF

    # Create start.sh
    cat << 'EOF' > /app/start.sh
#!/bin/bash
nginx -c /app/nginx.conf
/app/bin/auth_svc &
python3 /app/audit.py &
EOF
    chmod +x /app/start.sh

    # Generate corpora
    cat << 'EOF' > /app/gen_corpus.py
import json
import jwt
import base64

secret = "SUP3R_S3CR3T_HMAC_K3Y_9912"
wrong_secret = "WRONG_KEY_123"

def write_log(path, token):
    with open(path, "w") as f:
        json.dump({"request_id": "REQ_X", "headers": {"Authorization": f"Bearer {token}"}}, f)

# Clean
for i in range(10):
    token = jwt.encode({"username": "alice", "role": "user"}, secret, algorithm="HS256")
    write_log(f"/app/corpus/clean/log_{i:03d}.json", token)

# Evil - alg: none
for i in range(5):
    header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode('utf-8').rstrip('=')
    payload = base64.urlsafe_b64encode(b'{"username":"alice","role":"user"}').decode('utf-8').rstrip('=')
    token = f"{header}.{payload}."
    write_log(f"/app/corpus/evil/log_none_{i:03d}.json", token)

# Evil - wrong key
for i in range(5):
    token = jwt.encode({"username": "alice", "role": "user"}, wrong_secret, algorithm="HS256")
    write_log(f"/app/corpus/evil/log_wrong_{i:03d}.json", token)

# Evil - XSS/SQLi
payloads = [
    {"username": "admin' --", "role": "user"},
    {"username": "alice", "role": "<script>alert(1)</script>"},
    {"username": "bob", "role": "javascript:alert(1)"},
    {"username": "' OR 1=1", "role": "admin"},
    {"username": "admin", "role": "admin' OR '1'='1"}
]
for i, p in enumerate(payloads):
    token = jwt.encode(p, secret, algorithm="HS256")
    write_log(f"/app/corpus/evil/log_xss_{i:03d}.json", token)
EOF
    python3 /app/gen_corpus.py
    rm /app/gen_corpus.py

    useradd -m -s /bin/bash user || true
    su - user -c "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"

    chmod -R 777 /home/user