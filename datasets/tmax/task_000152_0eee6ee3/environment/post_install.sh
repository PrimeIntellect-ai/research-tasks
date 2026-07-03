apt-get update && apt-get install -y python3 python3-pip openssl faketime curl
pip3 install pytest

mkdir -p /home/user/clients
mkdir -p /home/user/service
cd /home/user

# 1. Generate CA
openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.pem -days 365 -nodes -subj "/CN=Internal_Root_CA" 2>/dev/null

# 2. Generate Client Certs
# Invalid 1: Expired (using faketime to generate a cert in the past)
openssl req -newkey rsa:2048 -keyout clients/client_1.key -out clients/client_1.csr -nodes -subj "/CN=Client1" 2>/dev/null
faketime '2020-01-01' openssl x509 -req -in clients/client_1.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out clients/client_1.crt -days 365 2>/dev/null

# Invalid 2: Wrong CA (Self-signed)
openssl req -x509 -newkey rsa:2048 -keyout clients/client_2.key -out clients/client_2.crt -days 365 -nodes -subj "/CN=Client2" 2>/dev/null

# Valid: Correctly signed and valid
openssl req -newkey rsa:2048 -keyout clients/client_3.key -out clients/client_3.csr -nodes -subj "/CN=Client3" 2>/dev/null
openssl x509 -req -in clients/client_3.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out clients/client_3.crt -days 365 2>/dev/null

# Invalid 3: Another Wrong CA
openssl req -x509 -newkey rsa:2048 -keyout fake_ca.key -out fake_ca.pem -days 365 -nodes -subj "/CN=Fake_CA" 2>/dev/null
openssl req -newkey rsa:2048 -keyout clients/client_4.key -out clients/client_4.csr -nodes -subj "/CN=Client4" 2>/dev/null
openssl x509 -req -in clients/client_4.csr -CA fake_ca.pem -CAkey fake_ca.key -CAcreateserial -out clients/client_4.crt -days 365 2>/dev/null

# 3. Create Secrets File
cat << 'EOF' > /home/user/service/internal_secrets.txt
User: Alice Dept: HR CC: 1234-5678-9012-3456
User: Bob Dept: IT CC: 9876 5432 1098 7654
User: Charlie Dept: Sales ID: 99823
User: Dave Dept: Exec CC: 1111-2222-3333-4444
EOF

# 4. Create Access Log
cat << 'EOF' > /home/user/service/access.log
192.168.1.10 - - [10/Oct/2023:13:55:36 -0700] "GET / HTTP/1.1" 200 2326
10.0.0.5 - - [10/Oct/2023:13:55:40 -0700] "GET /admin HTTP/1.1" 403 120
10.0.0.5 - - [10/Oct/2023:13:55:41 -0700] "GET /admin/config HTTP/1.1" 403 120
10.0.0.5 - - [10/Oct/2023:13:55:42 -0700] "GET /admin/users HTTP/1.1" 403 120
10.0.0.5 - - [10/Oct/2023:13:55:43 -0700] "GET /admin/secrets HTTP/1.1" 403 120
172.16.0.2 - - [10/Oct/2023:13:56:00 -0700] "GET /fetch_audit HTTP/1.1" 403 120
172.16.0.2 - - [10/Oct/2023:13:56:01 -0700] "GET /fetch_audit HTTP/1.1" 403 120
192.168.1.15 - - [10/Oct/2023:13:56:05 -0700] "GET / HTTP/1.1" 200 2326
EOF

# 5. Create vulnerable python server script
cat << 'EOF' > /home/user/service/server.py
import http.server, ssl, os, urllib.parse

class VulnerableHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/fetch_audit":
            qs = urllib.parse.parse_qs(parsed.query)
            if 'log' in qs:
                # Directory Traversal Vulnerability
                filepath = os.path.join(os.getcwd(), qs['log'][0])
                try:
                    with open(filepath, 'rb') as f:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(f.read())
                    return
                except:
                    pass
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not Found")

httpd = http.server.HTTPServer(('127.0.0.1', 8443), VulnerableHandler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="/home/user/ca.pem", keyfile="/home/user/ca.key")
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile="/home/user/ca.pem")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
os.chdir("/home/user/service")
httpd.serve_forever()
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user