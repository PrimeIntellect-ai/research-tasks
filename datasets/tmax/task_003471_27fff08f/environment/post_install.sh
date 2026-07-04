apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user/app_dir
    mkdir -p /home/user/.hidden_vault

    cat << 'EOF' > /home/user/.hidden_vault/admin_id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACD7w/zC7u4m1O9Y3Z1z4w2U7D2n7J4aX5T9V8c2o7H2XwAAAIi8y+2PvMvt
jwAAAAtzc2gtZWQyNTUxOQAAACD7w/zC7u4m1O9Y3Z1z4w2U7D2n7J4aX5T9V8c2o7H2Xw
AAAEDM8b1q5L2+w/yv3p9z0g8T9Y9X5u8T8G9M1Z7w9X8c3P3D/MLu7ibU71jdnXPjDZT
sPafsnhpflP1XxzajsfZfAAAAE2FkbWluQG1vY2stbWFjaGluZQECAwQ=
-----END OPENSSH PRIVATE KEY-----
EOF

    cat << 'EOF' > /home/user/auth_logs.txt
[2023-10-01 10:14:22] POST /login - User: guest - Status: 401 - Token: None
[2023-10-01 10:15:05] POST /login - User: admin - Status: 401 - Token: None
[2023-10-01 10:22:11] POST /login - User: test - Status: 401 - Token: None
[2023-10-01 11:05:33] POST /login - User: admin - Status: 200 - Token: 8f4e2d1c9b5a
[2023-10-01 11:10:02] POST /login - User: guest - Status: 401 - Token: None
EOF

    cat << 'EOF' > /home/user/app_dir/server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os

class VulnerableHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/api/fetch':
            token = self.headers.get('X-Admin-Token')
            if token != '8f4e2d1c9b5a':
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Forbidden: Invalid or missing token")
                return

            query = urllib.parse.parse_qs(parsed_path.query)
            filename = query.get('file', [''])[0]

            if not filename:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Bad Request: Missing file parameter")
                return

            # Vulnerable to path traversal
            target_path = os.path.join(os.getcwd(), filename)
            try:
                with open(target_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

if __name__ == '__main__':
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, VulnerableHandler)
    os.chdir('/home/user/app_dir')
    httpd.serve_forever()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user