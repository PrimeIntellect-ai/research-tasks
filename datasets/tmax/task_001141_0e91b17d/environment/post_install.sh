apt-get update && apt-get install -y python3 python3-pip nodejs
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/waf /home/user/backend

    cat << 'EOF' > /home/user/backend/server.js
const http = require('http');

const FLAG = "FLAG{jwt_evasion_master_9921}";

const server = http.createServer((req, res) => {
    if (req.url === '/api/admin/flag') {
        const auth = req.headers['authorization'];
        if (!auth || !auth.startsWith('Bearer ')) {
            res.writeHead(401);
            return res.end('Missing token');
        }

        const token = auth.split(' ')[1];
        const parts = token.split('.');

        if (parts.length < 2) {
            res.writeHead(400);
            return res.end('Invalid token format');
        }

        try {
            const headerStr = Buffer.from(parts[0], 'base64url').toString('utf8');
            const payloadStr = Buffer.from(parts[1], 'base64url').toString('utf8');

            const header = JSON.parse(headerStr);
            const payload = JSON.parse(payloadStr);

            if (header.alg && header.alg.toLowerCase() === 'none') {
                if (payload.role === 'admin') {
                    res.writeHead(200);
                    return res.end(FLAG);
                } else {
                    res.writeHead(403);
                    return res.end('Not an admin');
                }
            } else {
                res.writeHead(401);
                return res.end('Invalid signature');
            }
        } catch (e) {
            res.writeHead(400);
            return res.end('Malformed JSON');
        }
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(8081, '127.0.0.1');
EOF

    cat << 'EOF' > /home/user/waf/waf.py
import http.server
import urllib.request
import re
import base64
import sys

class WAFProxy(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            parts = token.split('.')
            if len(parts) >= 1:
                try:
                    # Pad for base64 decoding if necessary
                    header_b64 = parts[0]
                    header_b64 += "=" * ((4 - len(header_b64) % 4) % 4)
                    decoded_header = base64.urlsafe_b64decode(header_b64).decode('utf-8')

                    # IDS Pattern Matching for alg=none
                    if re.search(r'"alg"\s*:\s*"none"', decoded_header, re.IGNORECASE):
                        self.send_response(403)
                        self.end_headers()
                        self.wfile.write(b"WAF Block: Malicious JWT alg=none detected")
                        return
                except Exception as e:
                    pass

        # Forward request to backend
        req = urllib.request.Request("http://127.0.0.1:8081" + self.path, method="GET")
        for k, v in self.headers.items():
            req.add_header(k, v)

        try:
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for k, v in response.getheaders():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(response.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())

if __name__ == '__main__':
    server = http.server.HTTPServer(('127.0.0.1', 8080), WAFProxy)
    server.serve_forever()
EOF

    chmod -R 777 /home/user