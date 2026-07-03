apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest flask

    # Install required system packages
    apt-get install -y iproute2 netcat-openbsd curl gcc socat

    mkdir -p /app

    # Create the oracle parser source
    cat << 'EOF' > /app/oracle_parser.c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main() {
    uint32_t uid;
    uint8_t name_len;
    char username[32];
    uint16_t perms;

    while (1) {
        if (fread(&uid, 4, 1, stdin) != 1) break;
        if (fread(&name_len, 1, 1, stdin) != 1) { printf("INVALID\n"); return 0; }
        if (name_len > 31) { printf("INVALID\n"); return 0; }
        if (name_len > 0) {
            if (fread(username, 1, name_len, stdin) != name_len) { printf("INVALID\n"); return 0; }
        }
        username[name_len] = '\0';
        if (fread(&perms, 2, 1, stdin) != 1) { printf("INVALID\n"); return 0; }

        uint32_t uid_host = ((uid >> 24) & 0xff) | ((uid << 8) & 0xff0000) | ((uid >> 8) & 0xff00) | ((uid << 24) & 0xff000000);
        uint8_t* p = (uint8_t*)&perms;
        uint16_t perms_host = p[0] | (p[1] << 8);

        printf("UID:%u UNAME:%s PERMS:%04x\n", uid_host, username, perms_host);
    }
    return 0;
}
EOF

    gcc /app/oracle_parser.c -o /app/oracle_parser
    chmod +x /app/oracle_parser

    # Create Flask API
    cat << 'EOF' > /app/api.py
from flask import Flask, request
app = Flask(__name__)

@app.route('/sync', methods=['POST'])
def sync():
    with open('/tmp/api_received.log', 'wb') as f:
        f.write(request.data)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

    # Create Mock VM payload server
    cat << 'EOF' > /app/vm.py
import socket
import struct
import time

def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('10.0.0.2', 9999))
    s.listen(5)

    payload = struct.pack('>I', 1) + struct.pack('B', 4) + b'test' + struct.pack('<H', 0x1234)
    payload += struct.pack('>I', 2) + struct.pack('B', 5) + b'admin' + struct.pack('<H', 0xffff)

    while True:
        conn, addr = s.accept()
        try:
            conn.sendall(payload)
        except:
            pass
        conn.close()

if __name__ == '__main__':
    serve()
EOF

    # Create start_services.sh
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
# Start Flask API
python3 /app/api.py &

# Mock the VM network by adding the IP to loopback
ip addr add 10.0.0.2/24 dev lo 2>/dev/null || true

# Start Mock VM
python3 /app/vm.py &

# Wait a moment for services to bind
sleep 2
EOF
    chmod +x /app/start_services.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user