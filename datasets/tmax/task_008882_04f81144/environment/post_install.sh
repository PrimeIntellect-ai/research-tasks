apt-get update && apt-get install -y python3 python3-pip openssl
    pip3 install pytest requests

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/ca
    mkdir -p /home/user/server_certs

    # Create CA
    openssl req -x509 -newkey rsa:2048 -keyout /home/user/ca/ca.key -out /home/user/ca/ca.crt -days 365 -nodes -subj "/CN=Internal-CA"

    # Create Server Cert
    openssl req -newkey rsa:2048 -keyout /home/user/server_certs/server.key -out /home/user/server_certs/server.csr -nodes -subj "/CN=127.0.0.1"
    openssl x509 -req -in /home/user/server_certs/server.csr -CA /home/user/ca/ca.crt -CAkey /home/user/ca/ca.key -CAcreateserial -out /home/user/server_certs/server.crt -days 365

    # Create Vulnerable Server (server.py)
    cat << 'EOF' > /home/user/server.py
import ssl
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

class VulnHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/flag':
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
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
                # Vulnerable JWT parsing (alg=none bypass)
                header = json.loads(base64.urlsafe_b64decode(parts[0] + '==').decode('utf-8'))
                payload = json.loads(base64.urlsafe_b64decode(parts[1] + '==').decode('utf-8'))

                if header.get('alg', '').lower() == 'none' and payload.get('role') == 'admin':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "vulnerable", "flag": "FLAG{alg_none_mtls_bypass_success}"}).encode())
                    return
            except Exception as e:
                pass

            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'{"error": "Forbidden"}')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('127.0.0.1', 8443)
    httpd = HTTPServer(server_address, VulnHandler)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='/home/user/server_certs/server.crt', keyfile='/home/user/server_certs/server.key')
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='/home/user/ca/ca.crt')

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
EOF

    chmod -R 777 /home/user