apt-get update && apt-get install -y python3 python3-pip redis-server gcc
pip3 install pytest redis

mkdir -p /app/services

cat << 'EOF' > /app/services/config.json
{
    "producer_redis_port": 6380,
    "consumer_redis_port": 6381
}
EOF

cat << 'EOF' > /app/services/producer.py
import redis
import json
import sys

with open('/app/services/config.json') as f:
    config = json.load(f)

try:
    r = redis.Redis(host='localhost', port=config['producer_redis_port'])
    r.ping()
    r.lpush('fasta_queue', '>seq1 prior=0.5\nACGT')
    print("Producer OK")
except Exception as e:
    print(f"Producer failed: {e}")
    sys.exit(1)
EOF

cat << 'EOF' > /app/services/consumer.py
import redis
import json
import sys

with open('/app/services/config.json') as f:
    config = json.load(f)

try:
    r = redis.Redis(host='localhost', port=config['consumer_redis_port'])
    r.ping()
    item = r.brpop('fasta_queue', timeout=2)
    if item:
        with open('/home/user/pipeline_success.log', 'w') as f:
            f.write("PIPELINE_OK\n")
        print("Consumer OK")
    else:
        print("Consumer timeout")
        sys.exit(1)
except Exception as e:
    print(f"Consumer failed: {e}")
    sys.exit(1)
EOF

cat << 'EOF' > /app/services/start.sh
#!/bin/bash
redis-server --daemonize yes
sleep 1
python3 /app/services/producer.py &
PROD_PID=$!
python3 /app/services/consumer.py &
CONS_PID=$!

wait $PROD_PID
PROD_STATUS=$?
wait $CONS_PID
CONS_STATUS=$?

if [ $PROD_STATUS -eq 0 ] && [ $CONS_STATUS -eq 0 ]; then
    exit 0
else
    exit 1
fi
EOF
chmod +x /app/services/start.sh

cat << 'EOF' > /app/oracle_parser.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char seq_id[100] = {0};
    double prior = 0.0;
    int has_seq = 0;
    long gc_count = 0;
    long total_count = 0;

    int c;
    int in_header = 0;
    char header_line[1024];
    int h_idx = 0;

    while ((c = fgetc(stdin)) != EOF) {
        if (c == '>') {
            if (has_seq) {
                double gc_ratio = (total_count > 0) ? (double)gc_count / total_count : 0.0;
                double posterior = gc_ratio * prior;
                printf("%s posterior=%.4f\n", seq_id, posterior);
            }
            in_header = 1;
            h_idx = 0;
            has_seq = 0;
        } else if (in_header) {
            if (c == '\n') {
                header_line[h_idx] = '\0';
                if (sscanf(header_line, "%49s prior=%lf", seq_id, &prior) == 2) {
                    has_seq = 1;
                    gc_count = 0;
                    total_count = 0;
                }
                in_header = 0;
            } else {
                if (h_idx < 1023) {
                    header_line[h_idx++] = c;
                }
            }
        } else if (has_seq) {
            if (c == 'A' || c == 'T') {
                total_count++;
            } else if (c == 'C' || c == 'G') {
                total_count++;
                gc_count++;
            }
        }
    }
    if (has_seq) {
        double gc_ratio = (total_count > 0) ? (double)gc_count / total_count : 0.0;
        double posterior = gc_ratio * prior;
        printf("%s posterior=%.4f\n", seq_id, posterior);
    }
    return 0;
}
EOF
gcc -O3 /app/oracle_parser.c -o /app/oracle_parser

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app