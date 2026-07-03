apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        nginx \
        redis-server \
        curl \
        gcc \
        libssl-dev \
        openssl

    pip3 install --default-timeout=100 pytest flask redis python-dotenv requests

    # Create directories
    mkdir -p /app/nginx /app/flask /app/redis /app/certs

    # 1. Certificates
    cd /app/certs
    # Nginx certs
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx.key -out nginx.crt -subj "/CN=localhost"

    # Client chain and CRL
    # Create Root CA
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout root.key -out root.crt -subj "/CN=RootCA"
    # Create Intermediate CA (to be revoked)
    openssl req -new -nodes -newkey rsa:2048 \
        -keyout int.key -out int.csr -subj "/CN=IntermediateCA"
    # Create a v3 extension file for intermediate
    cat <<EOF > v3_ca.ext
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
basicConstraints=critical,CA:true
EOF
    openssl x509 -req -in int.csr -CA root.crt -CAkey root.key -CAcreateserial \
        -out int.crt -days 365 -extfile v3_ca.ext
    # Create Leaf
    openssl req -new -nodes -newkey rsa:2048 \
        -keyout leaf.key -out leaf.csr -subj "/CN=Leaf"
    openssl x509 -req -in leaf.csr -CA int.crt -CAkey int.key -CAcreateserial \
        -out leaf.crt -days 365

    # Create CRL revoking the intermediate
    mkdir -p demoCA/newcerts
    touch demoCA/index.txt
    echo 1000 > demoCA/crlnumber
    cat <<EOF > openssl_crl.cnf
[ ca ]
default_ca = CA_default
[ CA_default ]
dir = ./demoCA
database = \$dir/index.txt
crlnumber = \$dir/crlnumber
default_md = default
default_crl_days = 30
certificate = root.crt
private_key = root.key
EOF
    # Add int.crt to index.txt as revoked
    SERIAL=$(openssl x509 -in int.crt -noout -serial | cut -d= -f2)
    # Fake valid entry then revoke it
    echo "V	250101120000Z		$SERIAL	unknown	/CN=IntermediateCA" >> demoCA/index.txt
    openssl ca -config openssl_crl.cnf -revoke int.crt
    openssl ca -config openssl_crl.cnf -gencrl -out malware_crl.pem

    cat leaf.crt int.crt root.crt > client_chain.pem
    rm -rf demoCA root.* int.csr int.key leaf.* v3_ca.ext openssl_crl.cnf

    # 2. Obfuscator
    cat <<'EOF' > /app/obfuscator.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

int main() {
    unsigned char buffer[4096];
    size_t bytes_read;
    unsigned char *out_buf = NULL;
    size_t total_size = 0;

    while ((bytes_read = fread(buffer, 1, sizeof(buffer), stdin)) > 0) {
        out_buf = realloc(out_buf, total_size + bytes_read);
        for (size_t i = 0; i < bytes_read; i++) {
            out_buf[total_size + i] = buffer[i] ^ 0x42;
        }
        total_size += bytes_read;
    }

    if (total_size > 0) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256(out_buf, total_size, hash);
        fwrite(out_buf, 1, total_size, stdout);
        fwrite(hash, 1, SHA256_DIGEST_LENGTH, stdout);
    }
    free(out_buf);
    return 0;
}
EOF
    gcc /app/obfuscator.c -o /app/payload_obfuscator -lssl -lcrypto
    strip /app/payload_obfuscator
    rm /app/obfuscator.c

    cat <<'EOF' > /app/obfuscator_pseudo.c
// Decompiled pseudocode
void obfuscate_and_hash() {
    byte* data = read_stdin();
    for (int i = 0; i < len(data); i++) {
        data[i] = data[i] ^ 0x42;
    }
    byte hash[32] = sha256(data);
    write_stdout(data);
    write_stdout(hash);
}
EOF

    # 3. Services configuration
    # Nginx (intentionally broken/incomplete)
    cat <<'EOF' > /app/nginx/nginx.conf
events {}
http {
    server {
        listen 80;
        server_name localhost;
        # Missing SSL and proxy_pass configuration
        location / {
            return 200 "OK";
        }
    }
}
EOF

    # Redis (intentionally missing password)
    cat <<'EOF' > /app/redis/redis.conf
bind 127.0.0.1
port 6379
# requirepass supersecret
EOF

    # Flask app
    cat <<'EOF' > /app/flask/app.py
import os
import redis
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    password=os.environ.get('REDIS_PASSWORD', ''),
    decode_responses=True
)

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json.get('data')
    if data:
        r.set(data, "logged")
        # Vulnerable webhook call (CWE-295)
        try:
            requests.post("https://127.0.0.1:8443/webhook", json={"status": "logged"}, verify=False)
        except:
            pass
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "no data"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    cat <<'EOF' > /app/flask/.env
# REDIS_PASSWORD=
EOF

    cat <<'EOF' > /app/start_services.sh
#!/bin/bash
redis-server /app/redis/redis.conf &
nginx -c /app/nginx/nginx.conf &
cd /app/flask
export $(cat .env | xargs)
python3 app.py &
EOF
    chmod +x /app/start_services.sh

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app