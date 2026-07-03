apt-get update && apt-get install -y python3 python3-pip git gcc make redis-server libc6-dev libjson-c-dev
    pip3 install pytest flask redis requests

    mkdir -p /home/user/investigation/broker-repo
    mkdir -p /home/user/investigation/worker_src
    mkdir -p /app

    # Setup Git Forensics
    cd /home/user/investigation/broker-repo
    git config --global user.email "admin@local"
    git config --global user.name "Admin"
    git init

    cat << 'EOF' > broker.py
import flask
import redis
import json
import socket

app = flask.Flask(__name__)
with open('config.json') as f:
    config = json.load(f)

r = redis.Redis(host='localhost', port=6379, password=config.get('redis_pass', ''))

@app.route('/process', methods=['POST'])
def process():
    data = flask.request.json
    # Forward to worker
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', config.get('worker_port', 9000)))
        s.sendall(json.dumps(data).encode())
        resp = s.recv(4096)
        s.close()
        return resp
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(port=8080)
EOF

    cat << 'EOF' > config.json
{
    "redis_pass": "Sup3rS3cr3tT3l3m3try!",
    "worker_port": 9001
}
EOF
    git add broker.py config.json
    git commit -m "Initial commit"

    cat << 'EOF' > config.json
{
    "redis_pass": "",
    "worker_port": 9001
}
EOF
    git add config.json
    git commit -m "Remove hardcoded redis credentials"

    echo "# minor update" >> broker.py
    git add broker.py
    git commit -m "Minor update"

    # Setup C Bug and Oracle
    cat << 'EOF' > /app/oracle_worker.c
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main() {
    double a, c, d, R = 6371.0;
    // Dummy oracle
    return 0;
}
EOF
    gcc -o /app/oracle_worker /app/oracle_worker.c -lm
    rm /app/oracle_worker.c

    cat << 'EOF' > /home/user/investigation/worker_src/worker.c
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main() {
    float a, c, d, R = 6371.0f;
    // Dummy worker
    return 0;
}
EOF

    # Setup redis.conf
    cat << 'EOF' > /home/user/investigation/redis.conf
port 6379
daemonize no
EOF

    # Setup start_cluster.sh
    cat << 'EOF' > /home/user/investigation/start_cluster.sh
#!/bin/bash
redis-server /home/user/investigation/redis.conf &
cd /home/user/investigation/broker-repo && python3 broker.py &
/home/user/investigation/worker &
wait
EOF
    chmod +x /home/user/investigation/start_cluster.sh

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/investigation
    chmod -R 777 /home/user