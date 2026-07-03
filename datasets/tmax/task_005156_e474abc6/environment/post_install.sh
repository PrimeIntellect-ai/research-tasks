apt-get update && apt-get install -y python3 python3-pip redis-server curl
    pip3 install pytest redis flask

    mkdir -p /app
    mkdir -p /home/user

    # Create the oracle parser
    cat << 'EOF' > /app/oracle_parser
#!/usr/bin/env python3
import sys
import hashlib
import json

seen = set()
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split(',')
    if len(parts) != 4:
        continue
    ts, level, svc, msg = parts

    if level in ('TRACE', 'DEBUG'):
        continue

    hash_input = (svc + msg).encode('utf-8')
    h = hashlib.sha256(hash_input).hexdigest()

    if h in seen:
        continue
    seen.add(h)

    alert = True if level in ('ERROR', 'FATAL') else False

    out = {
        "alert": alert,
        "hash": h,
        "service": svc,
        "timestamp": ts
    }
    print(json.dumps(out, separators=(',', ':'), sort_keys=True))
EOF
    chmod +x /app/oracle_parser

    # Create generator config
    cat << 'EOF' > /home/user/generator_config.env
REDIS_PORT=6380
REDIS_KEY=incoming_logs
EOF

    # Create flask config
    cat << 'EOF' > /home/user/flask_config.env
REDIS_PORT=6379
REDIS_KEY=dev_logs
EOF

    # Create log generator
    cat << 'EOF' > /app/log_generator.py
#!/usr/bin/env python3
import os
import time
import redis
import random
import string
from datetime import datetime

def load_config(path):
    config = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    config[k] = v
    return config

config = load_config('/home/user/generator_config.env')
port = int(config.get('REDIS_PORT', 6379))
key = config.get('REDIS_KEY', 'incoming_logs')

try:
    r = redis.Redis(host='127.0.0.1', port=port, db=0)
    while True:
        ts = datetime.utcnow().isoformat()
        level = random.choice(['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'])
        svc = ''.join(random.choices(string.ascii_letters, k=5))
        msg = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        log_line = f"{ts},{level},{svc},{msg}"
        r.lpush(key, log_line)
        r.ltrim(key, 0, 99)
        time.sleep(0.5)
except Exception as e:
    pass
EOF
    chmod +x /app/log_generator.py

    # Create Flask API
    cat << 'EOF' > /app/flask_app.py
#!/usr/bin/env python3
import os
import redis
from flask import Flask, jsonify

app = Flask(__name__)

def load_config(path):
    config = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    config[k] = v
    return config

config = load_config('/home/user/flask_config.env')
port = int(config.get('REDIS_PORT', 6379))
key = config.get('REDIS_KEY', 'dev_logs')

r = redis.Redis(host='127.0.0.1', port=port, db=0)

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        logs = r.lrange(key, 0, -1)
        return jsonify([log.decode('utf-8') for log in logs])
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF
    chmod +x /app/flask_app.py

    # Create start_services.sh
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
pkill -f log_generator.py || true
pkill -f flask_app.py || true
service redis-server start || true

nohup python3 /app/log_generator.py > /dev/null 2>&1 &
nohup python3 /app/flask_app.py > /dev/null 2>&1 &
echo "Services started."
EOF
    chmod +x /app/start_services.sh

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user