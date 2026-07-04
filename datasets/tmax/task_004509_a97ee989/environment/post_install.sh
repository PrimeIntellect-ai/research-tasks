apt-get update && apt-get install -y python3 python3-pip redis-server nginx gcc curl
    pip3 install pytest flask redis

    mkdir -p /app/pipeline
    mkdir -p /home/user

    # Create Flask API
    cat << 'EOF' > /app/pipeline/api.py
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/data', methods=['POST'])
def data():
    content = request.json
    if content and 'value' in content:
        r.rpush('sensor_data', content['value'])
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "bad request"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    # Create start_pipeline.sh
    cat << 'EOF' > /app/pipeline/start_pipeline.sh
#!/bin/bash
# Start Redis
redis-server --daemonize yes

# Start Flask API
nohup python3 /app/pipeline/api.py > /tmp/flask.log 2>&1 &

# Start Nginx (Agent needs to configure nginx.conf and start it correctly)
# nginx -c /app/pipeline/nginx.conf
EOF
    chmod +x /app/pipeline/start_pipeline.sh

    # Create empty nginx.conf for the agent to modify
    touch /app/pipeline/nginx.conf

    # Create and compile oracle
    cat << 'EOF' > /app/oracle_stat.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    double x;
    long count = 0;
    double mean = 0.0;
    double M2 = 0.0;

    while (fscanf(f, "%lf", &x) == 1) {
        count += 1;
        double delta = x - mean;
        mean += delta / count;
        double delta2 = x - mean;
        M2 += delta * delta2;
    }
    fclose(f);

    double variance = 0.0;
    if (count > 1) {
        variance = M2 / (count - 1);
    }
    printf("Mean: %.8lf, Variance: %.8lf\n", mean, variance);
    return 0;
}
EOF
    gcc /app/oracle_stat.c -o /app/oracle_stat -O2
    chmod +x /app/oracle_stat

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app/pipeline