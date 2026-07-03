apt-get update && apt-get install -y python3 python3-pip nginx redis-server curl
    pip3 install pytest fastapi uvicorn redis python-dotenv

    mkdir -p /app/services/nginx
    mkdir -p /app/services/app

    cat << 'EOF' > /app/services/nginx/nginx.conf
events {}
http {
    server {
        listen 8080;
        location / {
            # TODO: Proxy to application server
            proxy_pass http://127.0.0.1:9999;
        }
    }
}
EOF

    cat << 'EOF' > /app/services/app/main.py
from fastapi import FastAPI
import redis
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

@app.get("/compute")
def compute():
    try:
        r.ping()
        return {"status": "success", "cache": "hit"}
    except:
        return {"status": "error", "cache": "miss"}
EOF

    cat << 'EOF' > /app/services/app/.env
REDIS_HOST=1.2.3.4
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app