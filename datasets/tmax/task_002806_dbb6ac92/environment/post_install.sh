apt-get update && apt-get install -y python3 python3-pip redis-server gcc libcurl4-openssl-dev libhiredis-dev curl
    pip3 install pytest flask redis

    mkdir -p /app
    cat << 'EOF' > /app/config_service.py
from flask import Flask
app = Flask(__name__)

@app.route('/window')
def window():
    return "10"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {
    int W = 10;
    double fallback_mean = 0.0;
    double history[10000];
    int count = 0;
    double val;

    while (scanf("%lf", &val) == 1) {
        double mean = 0.0;
        double std = 1.0;

        if (count == 0) {
            mean = fallback_mean;
            std = 1.0;
        } else {
            int n = (count < W) ? count : W;
            double sum = 0.0;
            for (int i = 0; i < n; i++) {
                sum += history[count - 1 - i];
            }
            mean = sum / n;

            if (n > 1) {
                double sq_sum = 0.0;
                for (int i = 0; i < n; i++) {
                    sq_sum += (history[count - 1 - i] - mean) * (history[count - 1 - i] - mean);
                }
                std = sqrt(sq_sum / (n - 1));
                if (std == 0.0) std = 1.0;
            }
        }

        printf("%.4f\n", (val - mean) / std);
        history[count++] = val;
    }
    return 0;
}
EOF
    gcc -O3 /opt/oracle/oracle.c -o /opt/oracle/normalize_stream_oracle -lm

    mkdir -p /var/lib/redis
    redis-server --daemonize yes --dir /var/lib/redis --dbfilename dump.rdb
    sleep 2
    redis-cli set fallback_mean 0.0
    redis-cli save
    pkill redis-server || true

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user