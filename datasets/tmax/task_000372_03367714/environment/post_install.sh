apt-get update && apt-get install -y python3 python3-pip procps socat
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/service
    ln -s /home/user/data/logs /home/user/service/logs

    cat << 'EOF' > /home/user/service/config.json
{"api_key": "secret_123"}
EOF

    cat << 'EOF' > /home/user/service/checker.py
import urllib.request
import json
import sys

try:
    with open('config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found. Make sure paths are correct.")
    sys.exit(1)

try:
    req = urllib.request.urlopen('http://127.0.0.1:9999/health', timeout=2)
    res = req.read().decode('utf-8')
except Exception as e:
    print("Connection failed:", e)
    sys.exit(1)

try:
    with open('/home/user/service/logs/result.json', 'w') as f:
        f.write(json.dumps({"success": True, "data": res.strip()}))
    print("Success: result.json written.")
except Exception as e:
    print("Write failed:", e)
    sys.exit(1)
EOF

    cat << 'EOF' > /home/user/service/backend.py
from http.server import BaseHTTPRequestHandler, HTTPServer
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BACKEND_OK")
HTTPServer(('127.0.0.1', 8080), Handler).serve_forever()
EOF

    chmod -R 777 /home/user