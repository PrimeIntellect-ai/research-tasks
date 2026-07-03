apt-get update && apt-get install -y python3 python3-pip redis-server
pip3 install pytest redis flask requests

mkdir -p /app

cat << 'EOF' > /app/redis.conf
port 6380
daemonize yes
EOF

cat << 'EOF' > /app/meta_service.py
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/path_info')
def path_info():
    path = request.args.get('path', '')
    # simple logic to return category based on path length or name
    cat = "unknown"
    if path:
        cat = f"cat_{path.strip('/')}"
    return jsonify({"category": cat})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

cat << 'EOF' > /app/oracle_analyzer
#!/usr/bin/env python3
import sys
import base64
import json
import redis
import requests

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    raw_bytes = base64.b64decode(line)

    decoded_str = None
    for enc in ['utf-8', 'utf-16le', 'latin-1']:
        try:
            decoded_str = raw_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue

    if decoded_str is None:
        continue

    parts = decoded_str.strip().split()
    if len(parts) < 4:
        continue

    ip = parts[0]
    path = parts[2]
    try:
        bytes_val = int(parts[3])
    except:
        bytes_val = 0

    try:
        score_str = r.get(f"ip:{ip}")
        threat_score = int(score_str) if score_str else 0
    except:
        threat_score = 0

    try:
        resp = requests.get(f"http://localhost:5000/path_info?path={path}", timeout=2)
        category = resp.json().get("category", "unknown")
    except:
        category = "unknown"

    risk_index = bytes_val * threat_score

    out = {"category": category, "ip": ip, "risk_index": risk_index}
    print(json.dumps(out, separators=(',', ':'), sort_keys=True))
EOF

chmod +x /app/oracle_analyzer

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user