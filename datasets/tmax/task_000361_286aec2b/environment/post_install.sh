apt-get update && apt-get install -y python3 python3-pip g++ libhiredis-dev nlohmann-json3-dev redis-server curl
    pip3 install pytest flask redis

    # Create service map
    mkdir -p /home/user
    cat << 'EOF' > /home/user/service_map.csv
service_code,service_name
SVC01,AuthService
SVC02,PaymentGateway
SVC03,InventoryManager
EOF

    # Create Python script to generate logs and golden file
    cat << 'EOF' > /opt/generate_data.py
import json
import random
import hashlib
import re

random.seed(42)

logs = []
for i in range(10000):
    log_id = hashlib.md5(str(i).encode()).hexdigest()
    level = random.choice(["INFO", "WARN", "ERROR"])
    service_code = random.choice(["SVC01", "SVC02", "SVC03", "SVC99"])
    message = "  " + random.choice(["User Logged IN!!", "DB connection failed...", "Timeout 504"]) + "  "
    logs.append({"log_id": log_id, "level": level, "service_code": service_code, "message": message})

duplicates = random.sample(logs, 2000)
final_logs = logs + duplicates
random.shuffle(final_logs)

with open("/opt/raw_logs.json", "w") as f:
    json.dump(final_logs, f)

service_map = {
    "SVC01": "AuthService",
    "SVC02": "PaymentGateway",
    "SVC03": "InventoryManager"
}

seen = set()
processed = []
for log in logs:
    log_id = log["log_id"]
    if log_id in seen:
        continue
    seen.add(log_id)

    level = log["level"]
    if level == "INFO":
        prefix = log_id[:4]
        val = int(prefix, 16)
        if val % 10 != 0:
            continue

    svc_code = log["service_code"]
    svc_name = service_map.get(svc_code, "UNKNOWN")

    msg = log["message"].lower()
    msg = re.sub(r'[^a-z0-9]', ' ', msg)
    msg = re.sub(r'\s+', ' ', msg).strip()

    processed.append({
        "log_id": log_id,
        "level": level,
        "service_code": svc_code,
        "service_name": svc_name,
        "message": msg
    })

with open("/opt/golden_processed_logs.jsonl", "w") as f:
    for p in processed:
        f.write(json.dumps(p) + "\n")
EOF

    python3 /opt/generate_data.py

    # Create log_generator.py
    cat << 'EOF' > /opt/log_generator.py
from flask import Flask
import redis
import json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/start', methods=['POST'])
def start():
    with open('/opt/raw_logs.json', 'r') as f:
        logs = json.load(f)
    for log in logs:
        r.rpush('raw_logs', json.dumps(log))
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

    # Create verifier
    cat << 'EOF' > /opt/verify.py
import json, sys

def load_logs(filepath):
    logs = set()
    with open(filepath, 'r') as f:
        for line in f:
            if not line.strip(): continue
            d = json.loads(line)
            logs.add(frozenset(d.items()))
    return logs

target = load_logs('/opt/golden_processed_logs.jsonl')
actual = load_logs('/home/user/processed_logs.jsonl')

intersection = len(target.intersection(actual))
union = len(target.union(actual))
jaccard = intersection / union if union > 0 else 0

print(f"Jaccard: {jaccard}")
if jaccard >= 0.99:
    sys.exit(0)
else:
    sys.exit(1)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user