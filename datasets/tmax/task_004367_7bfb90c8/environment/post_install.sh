apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install nginx, curl, and Rust
    apt-get install -y nginx curl cargo rustc

    # Create services directory and mock binaries
    mkdir -p /app/services

    cat << 'EOF' > /app/services/auth-svc
#!/bin/bash
python3 -c "
import http.server
import socketserver
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://127.0.0.1:8080/steal')
        self.end_headers()
with socketserver.TCPServer(('127.0.0.1', 8081), Handler) as httpd:
    httpd.serve_forever()
"
EOF
    chmod +x /app/services/auth-svc

    cat << 'EOF' > /app/services/token-logger
#!/bin/bash
python3 -c "
import http.server
import socketserver
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Logged')
with socketserver.TCPServer(('127.0.0.1', 9090), Handler) as httpd:
    httpd.serve_forever()
"
EOF
    chmod +x /app/services/token-logger

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user