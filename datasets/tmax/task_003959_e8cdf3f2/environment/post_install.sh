apt-get update && apt-get install -y python3 python3-pip git gcc make redis-server netcat curl
pip3 install pytest flask redis numpy requests

mkdir -p /app/libs
mkdir -p /app/services/backend_c
mkdir -p /app/services/api_gateway

# Create shared libraries
cat << 'EOF' > /app/libs/matrix_v1.c
void process_matrix(float *data, int size) {
    for (int i = 0; i < size; i++) {
        data[i] += 0.5;
    }
}
EOF

cat << 'EOF' > /app/libs/matrix_v2.c
void process_matrix(float *data, int size) {
    for (int i = 0; i < size; i++) {
        data[i] = data[i]; // Correct (dummy identity for simplicity)
    }
}
EOF

gcc -shared -o /app/libs/libmatrix_v1.so -fPIC /app/libs/matrix_v1.c
gcc -shared -o /app/libs/libmatrix_v2.so -fPIC /app/libs/matrix_v2.c
rm /app/libs/matrix_v1.c /app/libs/matrix_v2.c

# Create C backend
cat << 'EOF' > /app/services/backend_c/math_worker.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

void process_matrix(float *data, int size);

int main() {
    char *key = getenv("CALIBRATION_KEY");
    if (!key || strcmp(key, "0x9A4F2B1C") != 0) {
        // Incorrect key
    }

    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) exit(1);
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) exit(1);

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8001);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) exit(1);
    if (listen(server_fd, 3) < 0) exit(1);

    while(1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) continue;

        float buffer[100];
        int valread = read(new_socket, buffer, sizeof(buffer));
        if (valread > 0) {
            int size = valread / sizeof(float);
            process_matrix(buffer, size);
            if (!key || strcmp(key, "0x9A4F2B1C") != 0) {
                for(int i=0; i<size; i++) buffer[i] += 100.0; // Huge error if key is wrong
            }
            send(new_socket, buffer, valread, 0);
        }
        close(new_socket);
    }
    return 0;
}
EOF

cat << 'EOF' > /app/services/backend_c/Makefile
CC = gcc
CFLAGS = -Wall -fPIC
LDFLAGS = -L/app/libs -lmatrix_v1 -Wl,-rpath=/app/libs

all: math_worker

math_worker: math_worker.c
	$(CC) $(CFLAGS) -o math_worker math_worker.c $(LDFLAGS)

clean:
	rm -f math_worker
EOF

cd /app/services/backend_c
git init
git config user.email "dev@company.com"
git config user.name "Dev"
# Add hardcoded key
sed -i '1i #define CALIBRATION_KEY 0x9A4F2B1C' math_worker.c
git add math_worker.c Makefile
git commit -m "Initial commit"
# Remove hardcoded key
sed -i '/#define CALIBRATION_KEY 0x9A4F2B1C/d' math_worker.c
git add math_worker.c
git commit -m "Remove hardcoded calibration key"

# Create API Gateway
cat << 'EOF' > /app/services/api_gateway/app.py
from flask import Flask, request, jsonify
import socket
import struct

app = Flask(__name__)

@app.route('/invert', methods=['POST'])
def invert():
    data = request.json.get('matrix', [])

    # Send to C backend
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', 8001))
        packed_data = struct.pack(f'{len(data)}f', *data)
        s.sendall(packed_data)
        recv_data = s.recv(4096)
        s.close()

        unpacked_data = struct.unpack(f'{len(data)}f', recv_data)
        return jsonify({'result': unpacked_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
EOF

# Create evaluate script
cat << 'EOF' > /app/evaluate_mse.py
import requests
import numpy as np
import time

def run_eval():
    mse_total = 0
    for _ in range(10):
        matrix = np.random.rand(10).tolist()
        try:
            resp = requests.post('http://127.0.0.1:8000/invert', json={'matrix': matrix})
            res = resp.json().get('result', [])
            if not res:
                mse_total += 1000
                continue
            mse = np.mean((np.array(matrix) - np.array(res))**2)
            mse_total += mse
        except:
            mse_total += 1000

    print(f"FINAL_MSE: {mse_total/10}")

if __name__ == '__main__':
    run_eval()
EOF

# Create start script
cat << 'EOF' > /app/start_all.sh
#!/bin/bash
redis-server --daemonize yes
if [ -f /home/user/config.env ]; then
    source /home/user/config.env
    export CALIBRATION_KEY
fi
cd /app/services/backend_c
make clean && make
./math_worker &
cd /app/services/api_gateway
python3 app.py &
sleep 2
EOF
chmod +x /app/start_all.sh

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app