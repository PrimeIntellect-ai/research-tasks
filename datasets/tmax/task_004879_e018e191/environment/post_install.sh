apt-get update && apt-get install -y python3 python3-pip curl
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/vuln_app

    cat << 'EOF' > /home/user/vuln_app/auth.log
[INFO] 2023-10-10 10:00:01 - User 'guest' logged in.
[INFO] 2023-10-10 10:05:23 - User 'developer' logged in.
[WARN] 2023-10-10 10:15:45 - Failed login attempt for user 'admin_neo_77' (role=admin) from 192.168.1.105.
[INFO] 2023-10-10 10:20:00 - User 'test' logged in.
EOF

    cat << 'EOF' > /home/user/vuln_app/server.py
import json
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

FLAG = "FLAG{jwt_alg_none_1s_d4ng3r0us_9921}"

def decode_b64url(s):
    s = s.replace('-', '+').replace('_', '/')
    padding = '=' * (4 - (len(s) % 4))
    return base64.b64decode(s + padding)

class VulnerableHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/flag':
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                self.send_error(401, "Missing or invalid Authorization header")
                return

            token = auth_header.split(' ')[1]
            parts = token.split('.')
            if len(parts) != 3:
                self.send_error(400, "Malformed JWT")
                return

            try:
                header = json.loads(decode_b64url(parts[0]))
                payload = json.loads(decode_b64url(parts[1]))
            except Exception:
                self.send_error(400, "Invalid base64url encoding")
                return

            # Vulnerability: Accepts alg=none without verifying signature
            if header.get('alg', '').lower() == 'none':
                if payload.get('username') == 'admin_neo_77':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"flag": FLAG}).encode())
                    return
                else:
                    self.send_error(403, "Not authorized. Must be admin.")
                    return
            else:
                # Mock strict check for other algs
                if parts[2] != "valid_signature":
                    self.send_error(401, "Invalid signature")
                    return
                self.send_error(403, "Not authorized.")
        else:
            self.send_error(404, "Not found")

if __name__ == '__main__':
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, VulnerableHandler)
    httpd.serve_forever()
EOF

    chmod -R 777 /home/user