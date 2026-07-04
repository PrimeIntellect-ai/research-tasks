apt-get update && apt-get install -y python3 python3-pip openssl
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/investigation

    # 1. Create auth_logs.log
    cat << 'EOF' > /home/user/investigation/auth_logs.log
[INFO] User alice attempt with token: Bearer eyJ1c2VybmFtZSI6ICJhbGljZSIsICJyb2xlIjogInVzZXIifQ==
[INFO] User bob attempt with token: Bearer eyJ1c2VybmFtZSI6ICJib2IiLCAicm9sZSI6ICJ1c2VyIn0=
[WARN] User admin attempt with token: Bearer eyJ1c2VybmFtZSI6ICJhZG1pbiIsICJyb2xlIjogImFkbWluJChjYXQgL2V0Yy9wYXNzd2QpIn0=
[INFO] User charlie attempt with token: Bearer eyJ1c2VybmFtZSI6ICJjaGFybGllIiwgInJvbGUiOiAidXNlciJ9
EOF

    # 2. Create intercepted_chain.pem
    cd /home/user/investigation
    openssl req -x509 -newkey rsa:2048 -keyout root.key -out root.crt -days 365 -nodes -subj "/CN=Global Root CA"
    openssl req -newkey rsa:2048 -keyout proxy.key -out proxy.csr -nodes -subj "/CN=Evil Proxy Intercept CA"
    openssl x509 -req -in proxy.csr -CA root.crt -CAkey root.key -CAcreateserial -out proxy.crt -days 365
    openssl req -newkey rsa:2048 -keyout leaf.key -out leaf.csr -nodes -subj "/CN=internal-auth.local"
    openssl x509 -req -in leaf.csr -CA proxy.crt -CAkey proxy.key -CAcreateserial -out leaf.crt -days 365
    cat leaf.crt proxy.crt root.crt > /home/user/investigation/intercepted_chain.pem
    rm -f leaf.key proxy.key root.key leaf.csr proxy.csr root.crt proxy.crt leaf.crt *.srl
    cd /

    # 3. Create auth_server.py
    cat << 'EOF' > /home/user/investigation/auth_server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64

class AuthHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/authenticate':
            auth_header = self.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                try:
                    decoded = base64.b64decode(token).decode('utf-8')
                    if '$(cat /etc/passwd)' in decoded:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"flag": "FLAG{c0mm4nd_1nj3ct10n_byp4ss}"}).encode())
                        return
                except:
                    pass
        self.send_response(401)
        self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 8080), AuthHandler)
    server.serve_forever()
EOF
    chmod +x /home/user/investigation/auth_server.py

    chmod -R 777 /home/user