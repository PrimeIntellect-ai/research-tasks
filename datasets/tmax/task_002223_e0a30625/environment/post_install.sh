apt-get update && apt-get install -y python3 python3-pip nginx
pip3 install pytest flask gunicorn

mkdir -p /app/services

cat << 'EOF' > /app/oracle_planner
#!/usr/bin/env python3
import sys
from collections import defaultdict
import math

data = defaultdict(list)
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    if len(parts) != 4:
        continue
    ts, srv, metric, val_str = parts
    try:
        val = float(val_str)
    except ValueError:
        continue
    if val < 0:
        continue
    data[(srv, metric)].append(val)

for (srv, metric) in sorted(data.keys()):
    vals = data[(srv, metric)]
    max_val = max(vals)
    avg_val = math.floor(sum(vals) / len(vals))
    print(f"{srv} {metric} MAX: {max_val:.2f}, AVG: {avg_val}")
EOF
chmod +x /app/oracle_planner

cat << 'EOF' > /app/services/app.py
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
metrics_dir = os.environ.get('METRICS_DIR', '/tmp')
port = os.environ.get('PORT', '5000')

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    try:
        ts = data['timestamp']
        srv = data['service']
        metric = data['metric']
        val = data['value']
        line = f"{ts} {srv} {metric} {val}\n"
        log_file = os.path.join(metrics_dir, f"app_{port}.log")
        with open(log_file, 'a') as f:
            f.write(line)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=int(port))
EOF

cat << 'EOF' > /app/start_services.sh
#!/bin/bash
cd /app
export PORT=5001
gunicorn --bind 127.0.0.1:5001 "services.app:app" -D
export PORT=5002
gunicorn --bind 127.0.0.1:5002 "services.app:app" -D
EOF
chmod +x /app/start_services.sh

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user