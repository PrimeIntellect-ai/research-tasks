apt-get update && apt-get install -y python3 python3-pip openssl
    pip3 install pytest

    mkdir -p /home/user/ca /home/user/target_certs

    openssl req -x509 -newkey rsa:2048 -keyout /home/user/ca/root.key -out /home/user/ca/root.crt -days 365 -nodes -subj "/C=US/O=RedTeam/CN=RootCA"

    openssl req -newkey rsa:2048 -keyout /home/user/target_certs/client_alpha.key -out /home/user/target_certs/client_alpha.csr -nodes -subj "/C=US/O=RedTeam/CN=ClientAlpha"
    openssl x509 -req -in /home/user/target_certs/client_alpha.csr -CA /home/user/ca/root.crt -CAkey /home/user/ca/root.key -CAcreateserial -out /home/user/target_certs/client_alpha.crt -days 365

    openssl req -x509 -newkey rsa:2048 -keyout /home/user/target_certs/client_beta.key -out /home/user/target_certs/client_beta.crt -days 365 -nodes -subj "/C=US/O=RedTeam/CN=ClientBeta"

    openssl req -newkey rsa:2048 -keyout /home/user/ca/server.key -out /home/user/ca/server.csr -nodes -subj "/C=US/O=RedTeam/CN=127.0.0.1"
    openssl x509 -req -in /home/user/ca/server.csr -CA /home/user/ca/root.crt -CAkey /home/user/ca/root.key -CAcreateserial -out /home/user/ca/server.crt -days 365

    cat << 'EOF' > /home/user/server.py
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/auth':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'nonce-xyz123' https://vulnerable-jsonp.attacker.net;")
            self.end_headers()
            response = {"status": "authenticated", "session_id": "auth_tok_9988776655"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

httpd = HTTPServer(('127.0.0.1', 8443), AuthHandler)
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile='/home/user/ca/server.crt', keyfile='/home/user/ca/server.key')
context.load_verify_locations(cafile='/home/user/ca/root.crt')
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
EOF

    useradd -m -s /bin/bash user || true

    # Ensure the server starts when an interactive shell is spawned
    echo "python3 /home/user/server.py &" >> /home/user/.bashrc
    echo "python3 /home/user/server.py &" >> /root/.bashrc

    chmod -R 777 /home/user