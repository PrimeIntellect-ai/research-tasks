apt-get update && apt-get install -y python3 python3-pip redis-server git curl
    pip3 install pytest fastapi uvicorn redis pydantic pyinstaller

    mkdir -p /app
    cd /app

    # Create oracle source
    cat << 'EOF' > oracle.py
import sys

COEFF = 0x7F2A3B4C

def compute(n):
    if n == 0:
        return 1
    val = 1
    for i in range(1, n + 1):
        val = (val * COEFF) & 0xFFFFFFFF
        if val >= 0x80000000:
            val -= 0x100000000
    return val

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(compute(int(sys.argv[1])))
EOF

    # Build oracle
    pyinstaller --onefile oracle.py
    mv dist/oracle /app/oracle
    rm -rf build dist oracle.spec oracle.py

    # Initialize git
    git config --global user.email "dev@example.com"
    git config --global user.name "Dev"
    git init

    # Create api.py
    cat << 'EOF' > api.py
from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import uuid
import os
import time

app = FastAPI()
r = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0"))

class Job(BaseModel):
    value: int

@app.post("/compute")
def compute(job: Job):
    job_id = str(uuid.uuid4())
    r.rpush("jobs", json.dumps({"id": job_id, "value": job.value}))
    for _ in range(50):
        res = r.get(f"result_{job_id}")
        if res is not None:
            return {"result": int(res)}
        time.sleep(0.1)
    return {"error": "timeout"}
EOF

    # Create start.sh
    cat << 'EOF' > start.sh
#!/bin/bash
export REDIS_URL="redis://127.0.0.1:9999/0"
redis-server --daemonize yes
uvicorn api:app --host 127.0.0.1 --port 8000 &
python3 worker.py &
EOF
    chmod +x start.sh

    # Create working worker.py
    cat << 'EOF' > worker.py
import os
import redis
import json
import time

COEFF = 0x7F2A3B4C

def compute(n):
    if n == 0:
        return 1
    val = 1
    for i in range(1, n + 1):
        val = (val * COEFF) & 0xFFFFFFFF
        if val >= 0x80000000:
            val -= 0x100000000
    return val

def main():
    r = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0"))
    while True:
        job = r.lpop("jobs")
        if job:
            data = json.loads(job)
            res = compute(data["value"])
            r.set(f"result_{data['id']}", res)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
EOF

    git add .
    git commit -m "Initial commit with working worker"

    # Introduce bugs
    cat << 'EOF' > worker.py
import os
import redis
import json
import time

COEFF = 0

_cache = {}

def compute(n):
    if n in _cache:
        return _cache[n]
    if n == 0:
        return 1
    val = 1
    for i in range(1, n):
        val = (val * COEFF) & 0xFFFFFFFF
    _cache[n] = val
    return val

def main():
    r = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0"))
    while True:
        job = r.lpop("jobs")
        if job:
            data = json.loads(job)
            res = compute(data["value"])
            r.set(f"result_{data['id']}", res)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
EOF

    git add worker.py
    git commit -m "Remove hardcoded secret and optimize worker"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user