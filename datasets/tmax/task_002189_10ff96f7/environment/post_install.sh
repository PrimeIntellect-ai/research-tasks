apt-get update && apt-get install -y python3 python3-pip openssl curl net-tools iproute2 procps
    pip3 install pytest

    mkdir -p /opt/api
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /opt/api/server.key \
        -out /opt/api/server.crt \
        -subj "/CN=corp.auth.internal"

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/backend_logic.sh
#!/bin/bash
# Snippet of backend JWT validation logic

TOKEN=$1
HEADER=$(echo -n "$TOKEN" | cut -d '.' -f 1 | base64 -d 2>/dev/null)
PAYLOAD=$(echo -n "$TOKEN" | cut -d '.' -f 2 | base64 -d 2>/dev/null)
SIGNATURE=$(echo -n "$TOKEN" | cut -d '.' -f 3)

ALG=$(echo "$HEADER" | grep -oP '"alg"\s*:\s*"\K[^"]+')
AUD=$(echo "$PAYLOAD" | grep -oP '"aud"\s*:\s*"\K[^"]+')
ROLE=$(echo "$PAYLOAD" | grep -oP '"role"\s*:\s*"\K[^"]+')

# Vulnerability: Accepts 'none' algorithm and skips signature check
if [ "$ALG" = "none" ]; then
    # Signature verification bypassed
    IS_VALID=true
else
    # Mock signature check...
    IS_VALID=false
fi

# Verify Audience matches local certificate CN
EXPECTED_AUD=$(openssl x509 -in /opt/api/server.crt -noout -subject | grep -oP 'CN = \K.*')

if [ "$IS_VALID" = true ] && [ "$AUD" = "$EXPECTED_AUD" ] && [ "$ROLE" = "superuser" ]; then
    echo "Access Granted"
else
    echo "Access Denied"
fi
EOF

    cat << 'EOF' > /opt/api/server.py
import http.server
import ssl
import base64
import json
import re

FLAG = "FLAG{jwt_alg_none_privesc_7739}"

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/secure/flag':
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                self.send_error(401, 'Unauthorized')
                return

            token = auth_header.split(' ')[1]
            parts = token.split('.')
            if len(parts) != 3:
                self.send_error(401, 'Invalid token format')
                return

            try:
                # Add padding back for standard base64 decoding
                def decode_b64url(s):
                    s = s.replace('-', '+').replace('_', '/')
                    return base64.b64decode(s + '=' * (-len(s) % 4))

                header = json.loads(decode_b64url(parts[0]))
                payload = json.loads(decode_b64url(parts[1]))

                if header.get('alg', '').lower() == 'none' and \
                   payload.get('aud') == 'corp.auth.internal' and \
                   payload.get('role') == 'superuser' and \
                   parts[2] == '':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(FLAG.encode())
                    return
                else:
                    self.send_error(403, 'Forbidden')
                    return
            except Exception as e:
                self.send_error(401, 'Token decoding error')
                return
        else:
            self.send_error(404, 'Not Found')

server_address = ('127.0.0.1', 8443)
httpd = http.server.HTTPServer(server_address, RequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile='/opt/api/server.crt', keyfile='/opt/api/server.key')
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
EOF

    # Ensure the server starts when a bash shell is spawned
    cat << 'EOF' >> /etc/bash.bashrc
if ! pgrep -f "python3 /opt/api/server.py" > /dev/null; then
    nohup python3 /opt/api/server.py > /dev/null 2>&1 &
    sleep 1
fi
EOF

    chmod +x /home/user/backend_logic.sh
    chmod -R 777 /home/user