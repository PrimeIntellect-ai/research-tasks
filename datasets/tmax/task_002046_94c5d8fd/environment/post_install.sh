apt-get update && apt-get install -y python3 python3-pip nginx redis-server postgresql
    pip3 install pytest flask redis psycopg2-binary pymongo requests

    mkdir -p /home/user/data_pipeline

    cat << 'EOF' > /home/user/data_pipeline/nginx.conf
worker_processes 1;
events { worker_connections 1024; }
http {
    server {
        listen 8080;
        server_name localhost;

        # Missing /api/ location block
    }
}
EOF

    cat << 'EOF' > /home/user/data_pipeline/.env
REDIS_PORT=9999
PG_PORT=9999
MONGO_PORT=9999
FLASK_PORT=9999
EOF

    cat << 'EOF' > /home/user/data_pipeline/test_e2e.py
import requests
import os

print("Running E2E test...")
try:
    resp = requests.post("http://127.0.0.1:8080/api/ingest", json={"filepath": "/tmp/test.csv"})
    print(resp.status_code)
except Exception as e:
    print("Error:", e)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user