apt-get update && apt-get install -y python3 python3-pip curl jq make
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/mock_api.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MockAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/start':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "session_id": "sess-998877",
                "next_state": "AUTH",
                "challenge": "abcdef123"
            }).encode())
        elif self.path == '/api/data':
            auth_header = self.headers.get('Authorization')
            if auth_header == 'Bearer tok-secret-abc':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "items": [{"id": 1, "value": 42}, {"id": 2, "value": 15}, {"id": 3, "value": 100}],
                    "next_state": "SUBMIT"
                }).encode())
            else:
                self.send_response(401)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        data = json.loads(body) if body else {}

        if self.path == '/api/auth':
            if data.get('session_id') == 'sess-998877' and data.get('response') == '321fedcba':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "token": "tok-secret-abc",
                    "next_state": "FETCH"
                }).encode())
            else:
                self.send_response(400)
                self.end_headers()
        elif self.path == '/api/submit':
            if data.get('session_id') == 'sess-998877' and data.get('total_value') == 157:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "next_state": "DONE",
                    "flag": "FLAG{b4sh_st4t3_m4ch1n3_m4st3r}"
                }).encode())
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=MockAPIHandler, port=8080):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
EOF

    chmod -R 777 /home/user