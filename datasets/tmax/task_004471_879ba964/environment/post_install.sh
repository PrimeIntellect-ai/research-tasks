apt-get update && apt-get install -y python3 python3-pip redis-server
    pip3 install pytest flask gunicorn redis requests

    mkdir -p /app/verifier/corpus/evil
    mkdir -p /app/verifier/corpus/clean
    mkdir -p /home/user/incoming

    # Create Webhook API
    cat << 'EOF' > /app/webhook.py
from flask import Flask, request, jsonify
import redis
import json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.json
    r.rpush('ingested_data', json.dumps(data))
    return jsonify({"status": "ok"})
EOF

    # Create Startup Script
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
redis-server --daemonize yes
gunicorn --chdir /app -w 1 -b 127.0.0.1:8080 webhook:app --daemon
EOF
    chmod +x /app/start_services.sh

    # Create Sample Incoming Data
    cat << 'EOF' > /home/user/incoming/batch_01.json
[
  {
    "station_id": "ST-01",
    "timestamp": 1690000100,
    "temperature": 22.5,
    "humidity": null,
    "note": "Système normal 異常なし"
  }
]
EOF

    # Create User
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app