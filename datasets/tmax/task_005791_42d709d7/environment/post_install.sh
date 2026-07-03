apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create the C2 server script
    cat << 'EOF' > /tmp/c2_server.py
import http.server
import socketserver
import json

PORT = 8233

class C2Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/c2':
            cookie = self.headers.get('Cookie')
            custom = self.headers.get('X-C2-Auth')
            if cookie == 'AuthToken=Tr0j4n99' and custom == 'Active':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"payload": "EICAR_OR_SIMILAR_MALWARE_STRING"}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Unauthorized")
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("", PORT), C2Handler) as httpd:
    httpd.serve_forever()
EOF

    # Create the user and home directory
    useradd -m -s /bin/bash user || true

    # Create the traffic dump file
    cat << 'EOF' > /home/user/traffic_dump.txt
[Stream 1]
Source: 10.0.0.52
GET / HTTP/1.1
Host: 127.0.0.1:8233
User-Agent: Mozilla/5.0

HTTP/1.1 404 Not Found

[Stream 2]
Source: 198.51.100.45
GET /api/c2 HTTP/1.1
Host: 127.0.0.1:8233
Cookie: AuthToken=Tr0j4n99
X-C2-Auth: Active
User-Agent: curl/7.68.0

HTTP/1.1 200 OK
Content-type: application/json
{"payload": "EICAR_OR_SIMILAR_MALWARE_STRING"}

[Stream 3]
Source: 192.0.2.10
GET /api/c2 HTTP/1.1
Host: 127.0.0.1:8233
Cookie: AuthToken=WrongToken
X-C2-Auth: Active

HTTP/1.1 401 Unauthorized

[Stream 4]
Source: 203.0.113.88
GET /api/c2 HTTP/1.1
Host: 127.0.0.1:8233
Cookie: AuthToken=Tr0j4n99
X-C2-Auth: Active

HTTP/1.1 200 OK
Content-type: application/json
{"payload": "EICAR_OR_SIMILAR_MALWARE_STRING"}

[Stream 5]
Source: 198.51.100.45
GET /api/c2 HTTP/1.1
Host: 127.0.0.1:8233
Cookie: AuthToken=Tr0j4n99
X-C2-Auth: Active

HTTP/1.1 200 OK
EOF

    # Ensure the C2 server starts automatically when the container runs
    cat << 'EOF' > /.singularity.d/env/99-start-c2.sh
#!/bin/sh
if ! python3 -c 'import socket; s=socket.socket(); s.settimeout(0.1); exit(s.connect_ex(("127.0.0.1", 8233)))' 2>/dev/null; then
    nohup python3 /tmp/c2_server.py > /dev/null 2>&1 &
    sleep 0.5
fi
EOF
    chmod +x /.singularity.d/env/99-start-c2.sh

    chmod -R 777 /home/user