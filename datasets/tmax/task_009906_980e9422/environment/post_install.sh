apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/generate_log.py
import base64
from itertools import cycle
import random

def xor_crypt(text, key):
    return bytes([b ^ k for b, k in zip(text.encode('utf-8'), cycle(key.encode('utf-8')))])

def generate_token(timestamp, user, key):
    plaintext = f"{timestamp}:{user}"
    return base64.b64encode(xor_crypt(plaintext, key)).decode('utf-8')

users = ['alice', 'bob', 'charlie', 'diana']
secret_key = "Sup3rS3cr3tK3y"
malicious_key = "H4ck3rK3y99999"

malicious_ips = ["192.168.1.105", "10.0.45.22", "172.16.8.99"]

with open("/home/user/gateway.log", "w") as f:
    for i in range(1, 101):
        is_malicious = i in [14, 37, 82, 91] # random specific lines
        user = random.choice(users)
        timestamp = f"2024-10-12T{10+(i%10):02d}:{i%60:02d}:{i%60:02d}Z"

        if is_malicious:
            ip = random.choice(malicious_ips)
            token = generate_token(timestamp, user, malicious_key)
        else:
            ip = f"203.0.113.{i}"
            token = generate_token(timestamp, user, secret_key)

        log_line = f"{ip} - - [{timestamp}] \"GET /api/v1/data HTTP/1.1\" 200 - User: {user} Token: {token}\n"
        f.write(log_line)
EOF

    python3 /tmp/generate_log.py
    rm /tmp/generate_log.py

    chmod -R 777 /home/user