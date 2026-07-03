apt-get update && apt-get install -y python3 python3-pip procps curl
    pip3 install pytest

    mkdir -p /home/user/server
    cd /home/user/server

    cat << 'EOF' > server.py
import sys
import py_compile
from http.server import BaseHTTPRequestHandler, HTTPServer

token = sys.argv[2] if len(sys.argv) > 2 else "DEFAULT_TOKEN"

class AuditHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth_cookie = self.headers.get('Cookie', '')

        if self.path == '/':
            if f"auth_token={token}" in auth_cookie:
                self.send_response(200)
                self.send_header('X-Missing-CSP-Header', 'Content-Security-Policy is missing')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Welcome Admin. Download the latest module at /download/module.pyc")
            else:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Forbidden")
        elif self.path == '/download/module.pyc':
            if f"auth_token={token}" in auth_cookie:
                try:
                    with open("module.pyc", "rb") as f:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/x-python-code')
                        self.end_headers()
                        self.wfile.write(f.read())
                except FileNotFoundError:
                    self.send_response(404)
                    self.end_headers()
            else:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Forbidden")
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=AuditHandler, port=31337):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
EOF

    cat << 'EOF' > module.py
def get_secret():
    return "FLAG{pyc_str1ngs_r3v3rs3d}"
EOF

    python3 -c "import py_compile; py_compile.compile('module.py', cfile='module.pyc')"
    rm module.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user