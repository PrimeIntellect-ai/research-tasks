apt-get update && apt-get install -y python3 python3-pip g++ libssl-dev net-tools procps
    pip3 install pytest

    cat << 'EOF' > /tmp/malware_c2.py
from http.server import BaseHTTPRequestHandler, HTTPServer

class C2Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('X-Malware-Salt', 'r3K9')
        self.send_header('Set-Cookie', 'Evidence-Token=9e658bc795a2879f854a65ec01bf5eb0')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Unauthorized access logged.")

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8555), C2Handler)
    server.serve_forever()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user