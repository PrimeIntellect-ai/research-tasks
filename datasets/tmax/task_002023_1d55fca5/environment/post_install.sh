apt-get update && apt-get install -y python3 python3-pip redis-server curl strace
    pip3 install pytest flask redis simplejson

    mkdir -p /app

    cat << 'EOF' > /app/receiver.py
from flask import Flask, request
import redis
import json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_data()
    r.rpush('sensor_queue', data)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

    cat << 'EOF' > /app/worker.py
import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    item = r.blpop('sensor_queue', timeout=1)
    if item:
        _, data = item
        log = json.loads(data)
        # Bug 1: crash if missing metadata/status
        status = log['metadata']['status']
        # Bug 2: precision loss
        reading = float(log['sensor_reading'])
        log['sensor_reading'] = reading
        print(json.dumps(log))
    else:
        time.sleep(0.1)
EOF

    cat << 'EOF' > /app/oracle_processor
#!/usr/bin/env python3
import sys
import simplejson as json
from decimal import Decimal

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        data = json.loads(line, use_decimal=True)
        if 'metadata' not in data or 'status' not in data['metadata']:
            data['error'] = 'missing_status'
        print(json.dumps(data, use_decimal=True))
    except Exception as e:
        pass
EOF
    chmod +x /app/oracle_processor

    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
redis-server --daemonize yes
python3 /app/receiver.py &
python3 /app/worker.py &
wait
EOF
    chmod +x /app/start_services.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app