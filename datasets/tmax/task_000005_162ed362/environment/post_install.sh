apt-get update && apt-get install -y python3 python3-pip iptables systemd curl make build-essential
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app/datashaper-1.2.0
    mkdir -p /home/user/.config/systemd/user
    mkdir -p /home/user/.local/bin

    # Create worker.py
    cat << 'EOF' > /app/datashaper-1.2.0/worker.py
#!/usr/bin/env python3
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

if os.environ.get('DATA_ENV') != 'production':
    sys.exit(1)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8080), HealthHandler)
    server.serve_forever()
EOF
    chmod 644 /app/datashaper-1.2.0/worker.py

    # Create Makefile
    cat << 'EOF' > /app/datashaper-1.2.0/Makefile
install:
	mkdir -p /home/user/.local/bin
	install -m 644 worker.py /home/user/.local/bin/worker.py
EOF

    # Create systemd service
    cat << 'EOF' > /home/user/.config/systemd/user/datashaper.service
[Unit]
Description=Datashaper Service

[Service]
ExecStart=/home/user/.local/bin/worker.py
Restart=always

[Install]
WantedBy=default.target
EOF

    # Create oracle_transform
    cat << 'EOF' > /app/oracle_transform
#!/usr/bin/env python3
import sys

def rle(s):
    if not s:
        return ""
    res = []
    count = 1
    prev = s[0]
    for c in s[1:]:
        if c == prev:
            count += 1
        else:
            res.append(f"{count}{prev}")
            count = 1
            prev = c
    res.append(f"{count}{prev}")
    return "".join(res)

if __name__ == "__main__":
    data = sys.stdin.read().strip()
    rev = data[::-1]
    print(rle(rev))
EOF
    chmod +x /app/oracle_transform

    chown -R user:user /home/user
    chmod -R 777 /home/user