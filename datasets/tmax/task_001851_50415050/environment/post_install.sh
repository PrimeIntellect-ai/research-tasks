apt-get update && apt-get install -y python3 python3-pip redis-server
    pip3 install pytest fastapi uvicorn redis grpcio grpcio-tools

    mkdir -p /app/ingest /app/worker /app/data

    cat << 'EOF' > /app/ingest/main.py
from fastapi import FastAPI
import redis
import json

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0)

@app.post("/telemetry")
async def ingest(telemetry: list):
    for item in telemetry:
        r.lpush("telemetry_queue", json.dumps(item))
    return {"status": "ok"}
EOF

    cat << 'EOF' > /app/worker/main.py
import redis
import json
import time
from parser import parse_hex_tlv

r = redis.Redis(host='localhost', port=6379, db=0)

def main():
    while True:
        item = r.rpop("telemetry_queue")
        if item:
            data = json.loads(item)
            if "payload" in data:
                parse_hex_tlv(data["payload"])
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()
EOF

    cat << 'EOF' > /app/worker/parser.py
def parse_hex_tlv(hex_str):
    i = 0
    results = []
    while i < len(hex_str):
        tag = int(hex_str[i:i+2], 16)
        i += 2
        length = int(hex_str[i:i+2], 16)
        i += 2
        value = hex_str[i:i+length]
        i += length
        results.append({"tag": tag, "value": value})
    return results
EOF

    python3 -c '
import json
data = []
for i in range(2000):
    if i == 1342:
        data.append({"id": i, "payload": "0100"})
    else:
        data.append({"id": i, "payload": "0102AABB"})
with open("/app/data/failed_batch.json", "w") as f:
    json.dump(data, f)
'

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app