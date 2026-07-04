apt-get update && apt-get install -y python3 python3-pip redis-server gcc curl
    pip3 install pytest flask redis

    mkdir -p /home/user/app
    mkdir -p /home/user/oracle

    # Create api.py
    cat << 'EOF' > /home/user/app/api.py
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.json
    if 'raw_log' in data:
        r.lpush('log_queue_v2', data['raw_log'])
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "bad request"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
EOF

    # Create worker.py
    cat << 'EOF' > /home/user/app/worker.py
import redis
import json
import time
import subprocess

r = redis.Redis(host='localhost', port=6379, db=0)

def process_log(raw_log):
    process = subprocess.Popen(['python3', '/home/user/app/parser.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, _ = process.communicate(input=raw_log)
    try:
        parsed = json.loads(stdout.strip())
        with open('/home/user/app/parsed_logs.json', 'a') as f:
            f.write(json.dumps(parsed) + '\n')
    except json.JSONDecodeError:
        pass

if __name__ == '__main__':
    while True:
        log = r.rpop('log_queue_v1')
        if log:
            process_log(log.decode('utf-8'))
        time.sleep(0.5)
EOF

    # Create parser.py
    cat << 'EOF' > /home/user/app/parser.py
import sys
import json
import re

def parse(log):
    match = re.match(r'\[(.*?)\] (.*?) - (.*)', log)
    if match:
        return json.dumps({"timestamp": match.group(1), "level": match.group(2), "message": match.group(3)})
    return json.dumps({"error": "invalid format"})

if __name__ == '__main__':
    raw = sys.stdin.read().strip()
    print(parse(raw))
EOF

    # Create start.sh
    cat << 'EOF' > /home/user/app/start.sh
#!/bin/bash
redis-server --daemonize yes
python3 /home/user/app/api.py &
python3 /home/user/app/worker.py &
EOF
    chmod +x /home/user/app/start.sh

    # Create oracle C source and compile
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <string.h>

int main() {
    char buf[2048];
    if (fgets(buf, sizeof(buf), stdin) != NULL) {
        buf[strcspn(buf, "\n")] = 0;
        char ts[256] = {0};
        char lvl[256] = {0};
        char msg[1024] = {0};
        if (sscanf(buf, "[%255[^]]] %255s - %1023[^\n]", ts, lvl, msg) == 3) {
            printf("{\"timestamp\": \"%s\", \"level\": \"%s\", \"message\": \"%s\"}\n", ts, lvl, msg);
        } else {
            printf("{\"error\": \"invalid format\"}\n");
        }
    } else {
        printf("{\"error\": \"invalid format\"}\n");
    }
    return 0;
}
EOF
    gcc /tmp/oracle.c -o /home/user/oracle/parser_oracle
    chmod +x /home/user/oracle/parser_oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user