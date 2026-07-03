apt-get update && apt-get install -y python3 python3-pip nginx redis-server curl
    pip3 install pytest flask redis scapy

    mkdir -p /app/services
    mkdir -p /app/sandbox/bin
    mkdir -p /app/evidence

    # Create malicious nginx.conf
    cat << 'EOF' > /app/services/nginx.conf
events {}
http {
    server {
        listen 8080;
        location / {
            proxy_pass http://localhost:9999;
        }
    }
}
EOF

    # Create malicious .env
    cat << 'EOF' > /app/services/.env
REDIS_HOST=malicious.com
REDIS_PORT=1337
EOF

    # Create Flask app
    cat << 'EOF' > /app/services/app.py
from flask import Flask, jsonify
import os
import redis

app = Flask(__name__)

@app.route('/health')
def health():
    try:
        r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), db=0)
        r.ping()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

    # Create start.sh
    cat << 'EOF' > /app/services/start.sh
#!/bin/bash
redis-server --daemonize yes
nginx -c /app/services/nginx.conf
export $(cat /app/services/.env | xargs)
nohup python3 /app/services/app.py > /dev/null 2>&1 &
EOF
    chmod +x /app/services/start.sh

    # Create SUID binary
    cp /bin/bash /app/sandbox/bin/backup_util
    chmod 4755 /app/sandbox/bin/backup_util

    # Generate evidence and data using Python
    cat << 'EOF' > /tmp/setup.py
import os
from scapy.all import IP, TCP, Ether, wrpcap, Raw
import redis
import time

fragments = ["This is a ", "highly sensitive ", "document that ", "was fragmented ", "and exfiltrated."]
hashes = ["hash0", "hash1", "hash2", "hash3", "hash4"]

with open("/app/.secret_reference.txt", "w") as f:
    f.write("".join(fragments))

pkts = []
for i in range(5):
    req = f"GET / HTTP/1.1\r\nHost: localhost\r\nX-Exfil-Order: {i}\r\nCookie: session_hash={hashes[i]}\r\n\r\n"
    pkt = Ether()/IP(dst="127.0.0.1", src="127.0.0.1")/TCP(dport=8080, sport=10000+i)/Raw(load=req)
    pkts.append(pkt)

wrpcap("/app/evidence/traffic.pcap", pkts)

with open("/app/evidence/access.log", "w") as f:
    for i in range(5):
        f.write(f"127.0.0.1 - - [10/Oct/2023:13:55:36 -0700] \"GET / HTTP/1.1\" 200 123 \"-\" \"curl/7.68.0\" \"-\" X-Exfil-Order: {i} Cookie: session_hash={hashes[i]}\n")

# Start redis and populate
os.system("redis-server --daemonize yes")
time.sleep(2)
r = redis.Redis(host='localhost', port=6379, db=0)
for i in range(5):
    r.set(f"payload_{hashes[i]}", fragments[i])
r.save()
os.system("redis-cli shutdown")
EOF
    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user