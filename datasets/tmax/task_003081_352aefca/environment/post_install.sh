apt-get update && apt-get install -y python3 python3-pip redis-server tcpdump curl
    pip3 install pytest flask redis scapy requests

    mkdir -p /app/web
    mkdir -p /app/secrets
    mkdir -p /home/user

    # Create dummy secrets
    echo "secret_admin_data_123" > /app/secrets/admin.txt
    echo "secret_alice_data_456" > /app/secrets/alice.txt
    echo "secret_bob_data_789" > /app/secrets/bob.txt

    # Create Flask app
    cat << 'EOF' > /app/web/app.py
import os
import json
import hashlib
import uuid
from flask import Flask, request, jsonify, send_file
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

USERS = {
    "admin": "supersecret1",
    "alice": "password123",
    "bob": "qwerty"
}

@app.route('/login_v1', methods=['POST'])
def login_v1():
    # Deprecated endpoint, only logs attempts, doesn't actually auth
    return jsonify({"status": "deprecated"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = data.get('user')
    password = data.get('password')
    if user in USERS and USERS[user] == password:
        token = str(uuid.uuid4())
        r.set(token, user, ex=3600)
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}), 401

@app.route('/download', methods=['GET'])
def download():
    token = request.headers.get('Authorization')
    if not token or not r.exists(token):
        return jsonify({"error": "unauthorized"}), 401

    filename = request.args.get('file')
    if not filename:
        return jsonify({"error": "missing file parameter"}), 400

    # Vulnerable path traversal
    base_dir = "/app/web/public"
    filepath = os.path.join(base_dir, filename)

    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({"error": "file not found"}), 404

if __name__ == '__main__':
    os.makedirs("/app/web/public", exist_ok=True)
    with open("/app/web/public/hello.txt", "w") as f:
        f.write("hello world")
    app.run(host='127.0.0.1', port=5000)
EOF

    # Create start script
    cat << 'EOF' > /app/start.sh
#!/bin/bash
service redis-server start
cd /app/web && python3 app.py &
sleep 2
EOF
    chmod +x /app/start.sh

    # Create wordlist
    cat << 'EOF' > /home/user/wordlist.txt
password
123456
qwerty
password123
supersecret1
admin
letmein
EOF

    # Generate PCAP using scapy
    cat << 'EOF' > /tmp/gen_pcap.py
from scapy.all import *
import json
import hashlib

def make_request(user, pwd):
    h = hashlib.md5(f"{user}:{pwd}".encode()).hexdigest()
    payload = json.dumps({"user": user, "hash": h})
    req = f"POST /login_v1 HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nContent-Type: application/json\r\nContent-Length: {len(payload)}\r\n\r\n{payload}"

    ip = IP(src="192.168.1.100", dst="192.168.1.10")
    tcp = TCP(sport=12345, dport=5000, flags="PA")
    return ip/tcp/Raw(load=req)

pkts = [
    make_request("admin", "supersecret1"),
    make_request("alice", "password123"),
    make_request("bob", "qwerty")
]

wrpcap("/home/user/traffic.pcap", pkts)
EOF
    python3 /tmp/gen_pcap.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app