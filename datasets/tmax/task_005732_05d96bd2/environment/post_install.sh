apt-get update && apt-get install -y python3 python3-pip openssl build-essential libssl-dev
    pip3 install pytest

    mkdir -p /home/user/redteam_setup/certs
    cd /home/user/redteam_setup/certs

    # Generate CA
    openssl req -x509 -sha256 -nodes -days 3650 -newkey rsa:2048 -keyout rootCA.key -out rootCA.pem -subj "/C=US/ST=State/L=City/O=RedTeam/CN=RedTeam Root CA"

    # Generate Server cert
    openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/C=US/ST=State/L=City/O=RedTeam/CN=localhost"
    openssl x509 -req -in server.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out server.crt -days 365 -sha256

    cd /home/user/redteam_setup

    # Create wordlist and hash
    cat << 'EOF' > wordlist.txt
password123
admin
qwerty
redteam2024
specter99
dragon
letmein
EOF
    echo -n "specter99" | sha256sum | awk '{print $1}' > target_hash.txt

    # Create C2 Server script
    cat << 'EOF' > c2_server.py
import socket
import ssl
import hmac
import hashlib

HOST = '127.0.0.1'
PORT = 8443
PASSWORD = b'specter99'
MESSAGE = b'C2_SESSION_INIT'

def generate_expected_token():
    return hmac.new(PASSWORD, MESSAGE, hashlib.sha256).hexdigest()

def start_server():
    expected_token = generate_expected_token()

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='/home/user/redteam_setup/certs/server.crt', keyfile='/home/user/redteam_setup/certs/server.key')

    bindsocket = socket.socket()
    bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindsocket.bind((HOST, PORT))
    bindsocket.listen(5)

    while True:
        try:
            newsocket, fromaddr = bindsocket.accept()
            conn = context.wrap_socket(newsocket, server_side=True)
            data = conn.recv(1024).decode('utf-8').strip()

            if data == expected_token:
                conn.sendall(b"FLAG{evasion_payload_success_991823}")
            else:
                conn.sendall(b"UNAUTHORIZED")
        except Exception as e:
            pass
        finally:
            try:
                conn.close()
            except:
                pass

if __name__ == '__main__':
    start_server()
EOF
    chmod +x c2_server.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user