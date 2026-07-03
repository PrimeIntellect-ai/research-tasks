apt-get update && apt-get install -y python3 python3-pip openssh-client
    pip3 install pytest requests

    # Create directories
    mkdir -p /tmp/victim/uploads
    mkdir -p /tmp/victim/.ssh
    chmod 700 /tmp/victim/.ssh
    chmod 777 /tmp/victim/uploads

    # Create user
    useradd -m -s /bin/bash user || true

    # Create the vulnerable server script
    cat << 'EOF' > /home/user/server.py
import os
import re
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

UPLOAD_DIR = "/tmp/victim/uploads/"

class SimpleWAFHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/upload":
            self.send_error(404, "Not Found")
            return

        # 1. Cookie Inspection
        cookie_header = self.headers.get('Cookie', '')
        if 'session_role=admin' not in cookie_header:
            self.send_error(403, "Forbidden: Invalid Cookie")
            return

        # 2. Extract Filename
        filename = self.headers.get('X-File-Name', '')
        if not filename:
            self.send_error(400, "Bad Request: Missing X-File-Name header")
            return

        # 3. Pattern Matching Intrusion Detection (IDS)
        # Blocks literal "../" to prevent path traversal
        if re.search(r'\.\./', filename):
            self.send_error(403, "WAF Block: Path Traversal Detected")
            return

        # 4. Vulnerability: Unquoting after the IDS check
        decoded_filename = urllib.parse.unquote(filename)

        # 5. File writing
        target_path = os.path.join(UPLOAD_DIR, decoded_filename)
        target_dir = os.path.dirname(target_path)

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            file_data = self.rfile.read(content_length)

            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)

            with open(target_path, 'wb') as f:
                f.write(file_data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Upload successful")
        except Exception as e:
            self.send_error(500, str(e))

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8000), SimpleWAFHandler)
    server.serve_forever()
EOF

    chmod -R 777 /home/user