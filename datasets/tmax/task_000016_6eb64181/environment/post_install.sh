apt-get update && apt-get install -y python3 python3-pip acl curl
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app
    touch /app/auth_audio.wav

    mkdir -p /home/user/config

    cat << 'EOF' > /home/user/worker.sh
#!/bin/bash
sleep 2
echo "delta charlie seven" > /home/user/config/passcode.txt
EOF

    cat << 'EOF' > /home/user/api.py
import http.server
import socketserver
import os

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open('/home/user/config/passcode.txt', 'r') as f:
                passcode = f.read().strip()
        except Exception:
            self.send_response(500)
            self.end_headers()
            return

        auth = self.headers.get('Authorization')
        if auth == f'Bearer {passcode}':
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(401)
            self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(('127.0.0.1', 8080), Handler) as httpd:
    httpd.serve_forever()
EOF

    cat << 'EOF' > /home/user/api.sh
#!/bin/bash
python3 /home/user/api.py
EOF

    cat << 'EOF' > /home/user/start_services.sh
#!/bin/bash
bash /home/user/worker.sh &
bash /home/user/api.sh &
EOF

    chmod -R 777 /home/user
    chmod 700 /home/user/config
    chmod +x /home/user/*.sh