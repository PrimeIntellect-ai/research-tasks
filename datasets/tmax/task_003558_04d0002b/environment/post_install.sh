apt-get update && apt-get install -y python3 python3-pip cron nginx curl
    pip3 install pytest flask pyinstaller

    useradd -m -s /bin/bash user || true

    # Create directories
    mkdir -p /home/user/nginx /home/user/scripts /home/user/metrics_backup /home/user/data /app

    # Create dummy data
    echo "dummy database content" > /home/user/data/metrics.db

    # Create nginx config
    cat << 'EOF' > /home/user/nginx/nginx.conf
worker_processes 1;
events {
    worker_connections 1024;
}
http {
    server {
        listen 8080;
        location /api/metrics {
        }
    }
}
EOF

    # Create backup script
    cat << 'EOF' > /home/user/scripts/backup.sh
#!/bin/bash
cp data/metrics.db metrics.db.bak
EOF
    chmod +x /home/user/scripts/backup.sh

    # Setup crontab
    echo "* * * * * /home/user/scripts/backup.sh" | crontab -

    # Create Backend API
    cat << 'EOF' > /app/backend.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
EOF

    # Create Oracle Normalizer
    cat << 'EOF' > /app/oracle_source.py
#!/usr/bin/env python3
import sys
import json
import re

pattern = re.compile(r"^\[(.*?)\]\s+([A-Za-z0-9_]+):\s+([0-9\.\-]+)\s+tags=(.*)$")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    match = pattern.match(line)
    if match:
        ts, metric, value, tags = match.groups()
        try:
            val = float(value)
            print(json.dumps({"ts": ts, "metric": metric, "value": val, "tags": tags.split(",")}))
        except ValueError:
            print(json.dumps({"error": "invalid format"}))
    else:
        print(json.dumps({"error": "invalid format"}))
EOF

    pyinstaller --onefile /app/oracle_source.py --distpath /app --name oracle_normalizer
    chmod +x /app/oracle_normalizer

    # Start services in background for tests run in the same namespace if needed
    # (The verifier might rely on %startscript, so we provide it below)

    chmod -R 777 /home/user
    chmod -R 777 /app