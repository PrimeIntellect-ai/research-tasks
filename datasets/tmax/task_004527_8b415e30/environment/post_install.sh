apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick strace git nodejs npm fonts-dejavu-core
pip3 install pytest

mkdir -p /app/backend /app/frontend

# Create the image fixture
convert -size 400x200 xc:white -font DejaVu-Sans -pointsize 18 -fill black -draw "text 10,30 'System Architecture Diagram' text 10,60 '---------------------------' text 10,90 'API Gateway' text 10,120 'FRONTEND_PORT: 8080' text 10,150 'Worker Node' text 10,180 'BACKEND_PORT: 9090'" /app/architecture.png

# Setup Backend Repo
cd /app/backend
git init
git config user.email "test@example.com"
git config user.name "Test"

cat << 'EOF' > worker.js
const net = require('net');
const port = process.env.BACKEND_PORT || 9090;

function calculateData() {
    let sum = 0;
    for(let i = 0; i < 10; i++) {
        sum += i;
    }
    return sum;
}

const server = net.createServer((socket) => {
    socket.on('data', (data) => {
        const msg = data.toString().trim();
        if (msg === 'ping') {
            socket.write('pong\n');
        } else if (msg === 'data') {
            socket.write(calculateData() + '\n');
        }
    });
});

server.listen(port, '127.0.0.1', () => {
    console.log(`Backend listening on ${port}`);
});
EOF

git add worker.js
git commit -m "Initial commit v1.0"
git tag v1.0

# Add a few good commits
echo "// comment 1" >> worker.js && git commit -am "chore: update 1"
echo "// comment 2" >> worker.js && git commit -am "chore: update 2"

# Introduce the bug
cat << 'EOF' > worker.js
const net = require('net');
const port = process.env.BACKEND_PORT || 9090;

function calculateData() {
    let sum = 0;
    let i = 0;
    // BAD COMMIT: infinite loop
    while(i >= 0) { 
        sum += i;
        if(sum > 1000) break; // prevent actual infinite lockup during setup/test but functionally broken
    }
    return sum;
}

const server = net.createServer((socket) => {
    socket.on('data', (data) => {
        const msg = data.toString().trim();
        if (msg === 'ping') {
            socket.write('pong\n');
        } else if (msg === 'data') {
            socket.write(calculateData() + '\n');
        }
    });
});

server.listen(port, '127.0.0.1', () => {
    console.log(`Backend listening on ${port}`);
});
EOF
git commit -am "feat: refactor calculation"
BAD_COMMIT=$(git rev-parse HEAD)

# Add a few more commits
echo "// comment 3" >> worker.js && git commit -am "chore: update 3"
echo "// comment 4" >> worker.js && git commit -am "chore: update 4"
git branch -M main

# Store BAD_COMMIT somewhere secret for the test harness if needed
echo $BAD_COMMIT > /tmp/secret_bad_commit.txt

# Setup Frontend
cd /app/frontend
cat << 'EOF' > server.py
import os
import socket
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

FRONTEND_PORT = int(os.environ.get('FRONTEND_PORT', 8080))
BACKEND_PORT = int(os.environ.get('BACKEND_PORT', 9090))

# INTENTIONAL BUG: tries to write to root-owned dir
log_file = open('/var/log/frontend_app.log', 'a')

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', BACKEND_PORT))
                s.sendall(b'data\n')
                data = s.recv(1024).decode('utf-8').strip()
                s.close()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {"status": "ok", "backend_data": int(data)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

httpd = HTTPServer(('127.0.0.1', FRONTEND_PORT), RequestHandler)
httpd.serve_forever()
EOF

touch /var/log/frontend_app.log
chown root:root /var/log/frontend_app.log
chmod 600 /var/log/frontend_app.log

chmod -R 777 /app

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user