apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        nginx \
        redis-server \
        gcc \
        curl \
        socat \
        netcat

    pip3 install pytest flask redis

    mkdir -p /home/user/app/config
    mkdir -p /home/user/app/src
    mkdir -p /home/user/app/legacy
    mkdir -p /home/user/app/bin

    # Create start_services.sh
    cat << 'EOF' > /home/user/app/start_services.sh
#!/bin/bash
nginx -c /home/user/app/config/nginx.conf
redis-server --daemonize yes
python3 /home/user/app/config/flask_app.py &
source /home/user/app/config/backend.conf
socat TCP-LISTEN:$BIND_PORT,fork,reuseaddr EXEC:/home/user/app/bin/fraud_aggregator &
EOF
    chmod +x /home/user/app/start_services.sh

    # Create nginx.conf
    cat << 'EOF' > /home/user/app/config/nginx.conf
events {}
http {
    server {
        listen 8080;
        location / {
            proxy_pass http://localhost:5001;
        }
    }
}
EOF

    # Create flask_app.py
    cat << 'EOF' > /home/user/app/config/flask_app.py
from flask import Flask, request
import socket
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
BACKEND_PORT = 9001

@app.route('/api/fraud_status', methods=['POST'])
def fraud_status():
    payload = request.get_data()
    r.set('latest_payload', payload)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', BACKEND_PORT))
        s.sendall(payload)
        s.shutdown(socket.SHUT_WR)
        data = s.recv(1024)
        s.close()
        return data
    except Exception as e:
        return str(e), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

    # Create backend.conf
    cat << 'EOF' > /home/user/app/config/backend.conf
BIND_PORT=9005
EOF

    # Create oracle.c
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdint.h>

int main() {
    int32_t val;
    int32_t window[10] = {0};
    int count = 0;
    int index = 0;
    int32_t max_peak = -2147483648;
    long long total_sum = 0;

    while (fread(&val, sizeof(int32_t), 1, stdin) == 1) {
        window[index] = val;
        index = (index + 1) % 10;
        count++;
        total_sum += val;

        int limit = count < 10 ? count : 10;
        int32_t current_peak = window[0];
        for (int i = 1; i < limit; i++) {
            if (window[i] > current_peak) {
                current_peak = window[i];
            }
        }
        if (current_peak > max_peak || count == 1) {
            max_peak = current_peak;
        }
    }
    printf("Count: %d\nSum: %lld\nPeak: %d\n", count, total_sum, max_peak);
    return 0;
}
EOF
    gcc /tmp/oracle.c -o /home/user/app/legacy/oracle_aggregator
    chmod +x /home/user/app/legacy/oracle_aggregator

    # Create fraud_aggregator.c (with bug)
    cat << 'EOF' > /home/user/app/src/fraud_aggregator.c
#include <stdio.h>
#include <stdint.h>

int main() {
    int32_t val;
    int32_t window[10] = {0};
    int count = 0;
    int index = 0;
    int32_t max_peak = -2147483648;
    long long total_sum = 0;

    while (fread(&val, sizeof(int32_t), 1, stdin) == 1) {
        window[index] = val;
        index = (index + 1) % 11;
        count++;
        total_sum += val;

        int limit = count < 10 ? count : 10;
        int32_t current_peak = window[0];
        for (int i = 1; i < limit; i++) {
            if (window[i] > current_peak) {
                current_peak = window[i];
            }
        }
        if (current_peak > max_peak || count == 1) {
            max_peak = current_peak;
        }
    }
    printf("Count: %d\nSum: %lld\nPeak: %d\n", count, total_sum, max_peak);
    return 0;
}
EOF
    gcc /home/user/app/src/fraud_aggregator.c -o /home/user/app/bin/fraud_aggregator
    chmod +x /home/user/app/bin/fraud_aggregator

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/app
    chmod -R 777 /home/user