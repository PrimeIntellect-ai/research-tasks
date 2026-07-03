apt-get update && apt-get install -y python3 python3-pip redis-server nginx openssh-server curl sudo
    pip3 install pytest flask

    useradd -m -s /bin/bash user || true

    mkdir -p /app
    cat << 'EOF' > /app/app.py
from flask import Flask, request, jsonify
import json
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    if request.headers.get('X-Auditor-Check') != 'active':
        return jsonify({"status": "error", "message": "Missing header"}), 403

    with open('/app/config.json') as f:
        config = json.load(f)

    key_path = config.get("ssh_key_path")

    try:
        res = subprocess.run(["ssh", "-i", key_path, "-o", "StrictHostKeyChecking=no", "user@127.0.0.1"], capture_output=True, text=True, timeout=5)
        return jsonify({"status": "ok", "logs_read": True})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    cat << 'EOF' > /app/config.json
{
  "ssh_key_path": "/app/default_key"
}
EOF

    cat << 'EOF' > /app/nginx.conf
worker_processes 1;
events { worker_connections 1024; }
http {
    server {
        listen 8080;
        # Missing proxy_pass and header
    }
}
EOF

    cat << 'EOF' > /app/oracle_validator
#!/usr/bin/env python3
import sys
import re
import hashlib

if len(sys.argv) != 3:
    sys.exit(1)

cookie = sys.argv[1]
log_line = sys.argv[2]

if re.search(r'union\s+select', log_line, re.IGNORECASE) or \
   re.search(r'/etc/shadow', log_line, re.IGNORECASE) or \
   re.search(r'<script>', log_line, re.IGNORECASE):
    print("DENY_IDS")
    sys.exit(0)

pin = "4829"
h = hashlib.sha256((pin + cookie).encode()).hexdigest()
if h[-1] in ['a', 'b', 'c']:
    print("ALLOW")
else:
    print("DENY_AUTH")
EOF
    chmod +x /app/oracle_validator

    touch /var/log/syslog
    echo "dummy log" > /var/log/syslog

    mkdir -p /run/sshd

    chmod -R 777 /home/user