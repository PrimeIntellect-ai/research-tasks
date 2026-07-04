apt-get update && apt-get install -y python3 python3-pip curl
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/server.py
import json
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

def b64url_decode(inp):
    padding = '=' * (4 - (len(inp) % 4))
    return base64.urlsafe_b64decode(inp + padding)

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/flag':
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                self.send_response(401)
                self.end_headers()
                return

            token = auth_header.split(' ')[1]
            parts = token.split('.')
            if len(parts) != 3:
                self.send_response(400)
                self.end_headers()
                return

            try:
                header = json.loads(b64url_decode(parts[0]))
                payload = json.loads(b64url_decode(parts[1]))

                # Vulnerability: accepts 'none' algorithm and skips signature verification
                if header.get('alg', '').lower() == 'none':
                    pass # Skip signature check entirely
                else:
                    # Dummy signature check for simulation
                    if parts[2] != "valid_sig":
                        self.send_response(403)
                        self.end_headers()
                        return

                if payload.get('role') == 'admin':
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"FLAG{jwt_alg_none_byp4ss_1337}")
                else:
                    self.send_response(403)
                    self.end_headers()
                    self.wfile.write(b"Access denied. Admin role required.")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8080), AuthHandler)
    server.serve_forever()
EOF

    cat << 'EOF' > /home/user/api_logs.txt
[2023-10-12 10:00:01] GET /user/profile HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdHVzZXIiLCJyb2xlIjoidXNlciJ9.valid_sig
Status: 200

[2023-10-12 10:05:22] GET /settings HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiam9obiIsInJvbGUiOiJ1c2VyIn0.valid_sig
Status: 200

[2023-10-12 10:15:00] POST /login HTTP/1.1
Body: username=admin&password=incorrect
Status: 401
EOF

    chown user:user /home/user/server.py
    chown user:user /home/user/api_logs.txt

    chmod -R 777 /home/user
    chmod 755 /home/user/server.py