apt-get update && apt-get install -y python3 python3-pip redis-server redis-tools curl golang
    pip3 install pytest flask redis

    mkdir -p /app/emitter /app/webhook /opt/oracle

    # Create config.env
    cat << 'EOF' > /app/emitter/config.env
REDIS_HOST=redis_db
REDIS_PORT=6380
EOF

    # Create emitter.py
    cat << 'EOF' > /app/emitter/emitter.py
import os
import time
import uuid
import random
import redis

host = "redis_db"
port = 6380
with open("/app/emitter/config.env") as f:
    for line in f:
        if line.startswith("REDIS_HOST="): host = line.strip().split("=")[1]
        if line.startswith("REDIS_PORT="): port = int(line.strip().split("=")[1])

try:
    r = redis.Redis(host=host, port=port)
    while True:
        seq = "".join(random.choices(["A", "C", "T", "G"], k=random.randint(10, 50)))
        job_id = str(uuid.uuid4())
        r.rpush("dna_jobs", f"{job_id}|{seq}")
        time.sleep(1)
except Exception as e:
    print(e)
EOF

    # Create listener.py
    cat << 'EOF' > /app/webhook/listener.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/results', methods=['POST'])
def results():
    data = request.json
    with open("/app/webhook/results.log", "a") as f:
        f.write(f"{data.get('id')}:{data.get('result')}\n")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

    # Create start_services.sh
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
redis-server --daemonize yes
python3 /app/webhook/listener.py &
python3 /app/emitter/emitter.py &
EOF
    chmod +x /app/start_services.sh

    # Create and compile oracle
    cat << 'EOF' > /opt/oracle/analyze_oracle.go
package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		return
	}
	seq := os.Args[1]
	L := len(seq)
	X := make([]float64, L)
	for i, c := range seq {
		if c == 'G' || c == 'C' {
			X[i] = 1.0
		} else {
			X[i] = 0.0
		}
	}

	S := make([]float64, L)
	for i := 0; i < L; i++ {
		var left, right float64
		if i > 0 { left = X[i-1] }
		if i < L-1 { right = X[i+1] }
		S[i] = 0.25*left + 0.5*X[i] + 0.25*right
	}

	for i := 1; i < L-1; i++ {
		D := (S[i+1] - S[i-1]) / 2.0
		if i > 1 {
			fmt.Print(" ")
		}
		fmt.Printf("%.2f", D)
	}
	fmt.Println()
}
EOF
    cd /opt/oracle
    go build -o analyze_oracle analyze_oracle.go
    chmod +x analyze_oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /opt/oracle
    chmod -R 777 /home/user