apt-get update && apt-get install -y python3 python3-pip openssl nmap curl
pip3 install pytest

useradd -m -s /bin/bash user || true
mkdir -p /home/user

cat << 'EOF' > /home/user/wordlist.txt
password123
admin
qwerty
iloveyou
hunter2
secret
123456
EOF

openssl req -x509 -newkey rsa:2048 -keyout /home/user/server.key -out /home/user/server.crt -days 365 -nodes -subj "/C=US/ST=State/L=City/O=FLAG{C3rt_0rganizati0n_L3ak}/CN=localhost"

cat << 'EOF' > /home/user/https_server.py
import http.server
import ssl

server_address = ('localhost', 8443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               certfile='/home/user/server.crt',
                               keyfile='/home/user/server.key',
                               ssl_version=ssl.PROTOCOL_TLS)
httpd.serve_forever()
EOF

cat << 'EOF' > /home/user/http_auth_server.py
import http.server
import base64

class AuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        expected_auth = 'Basic ' + base64.b64encode(b'admin:hunter2').decode('utf-8')

        if auth_header == expected_auth:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'FLAG{Brut3_F0rc3_M4st3r}')
        else:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Restricted"')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Unauthorized')

server_address = ('localhost', 8080)
httpd = http.server.HTTPServer(server_address, AuthHandler)
httpd.serve_forever()
EOF

chmod -R 777 /home/user