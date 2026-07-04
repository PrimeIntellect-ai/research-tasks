apt-get update && apt-get install -y python3 python3-pip redis-server
    pip3 install pytest flask redis

    mkdir -p /app

    cat << 'EOF' > /app/oracle_parser
#!/usr/bin/env python3
import sys, struct, json
if len(sys.argv) != 2: sys.exit(1)
hex_str = sys.argv[1].strip()
b = bytes.fromhex(hex_str)
event_id, duration_ms = struct.unpack('<II', b)
print(json.dumps({"event_id": event_id, "duration_ms": duration_ms}))
EOF
    chmod +x /app/oracle_parser

    cat << 'EOF' > /app/log_parser.py
import sys, struct, json

def parse_log(hex_str):
    b = bytes.fromhex(hex_str)
    # BUG: using signed integer for duration_ms
    event_id, duration_ms = struct.unpack('<Ii', b)
    return {"event_id": event_id, "duration_ms": duration_ms}

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(json.dumps(parse_log(sys.argv[1].strip())))
EOF

    cat << 'EOF' > /app/api.py
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
# BUG: wrong port
r = redis.Redis(host='localhost', port=6380, db=0)

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.json
    if not data or 'log' not in data:
        return jsonify({"error": "missing log"}), 400
    r.lpush('log_queue', data['log'])
    return jsonify({"status": "queued"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

    cat << 'EOF' > /app/worker.py
import redis
import json
import time
import subprocess

# BUG: wrong port
r = redis.Redis(host='localhost', port=6380, db=0)

def main():
    while True:
        item = r.brpop('log_queue', timeout=1)
        if item:
            _, hex_str = item
            hex_str = hex_str.decode('utf-8')
            # Call parser
            result = subprocess.run(['python3', '/app/log_parser.py', hex_str], capture_output=True, text=True)
            if result.returncode == 0:
                with open('/app/processed_logs.json', 'a') as f:
                    f.write(result.stdout.strip() + '\n')
        time.sleep(0.1)

if __name__ == "__main__":
    main()
EOF

    chmod -R 777 /app
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user