apt-get update && apt-get install -y python3 python3-pip gcc gawk supervisor
    pip3 install pytest

    mkdir -p /app
    mkdir -p /etc/supervisor/conf.d
    mkdir -p /var/log/supervisor

    # Create the oracle C program
    cat << 'EOF' > /app/oracle_processor.c
#include <stdio.h>

int main() {
    long long n = 0;
    double mean = 0.0;
    double M2 = 0.0;
    double x;
    while (scanf("%lf", &x) == 1) {
        n++;
        double delta = x - mean;
        mean += delta / n;
        M2 += delta * (x - mean);
        printf("%lld %.4f %.4f\n", n, mean, M2);
    }
    return 0;
}
EOF
    gcc -O3 /app/oracle_processor.c -o /app/oracle_processor
    chmod +x /app/oracle_processor

    # Create log_gen.sh
    cat << 'EOF' > /app/log_gen.sh
#!/bin/bash
while true; do
    echo $((1000000000 + RANDOM % 500))
    sleep 0.1
done > /tmp/raw_logs
EOF
    chmod +x /app/log_gen.sh

    # Create log_alert.sh
    cat << 'EOF' > /app/log_alert.sh
#!/bin/bash
while read -r n mean ssd; do
    # Simulate some check
    if [[ "$ssd" == *"NaN"* || "$ssd" == *"-"* ]]; then
        echo "ALERT: Invalid stats at line $n" >&2
    else
        echo "OK: line $n mean=$mean ssd=$ssd"
    fi
done
EOF
    chmod +x /app/log_alert.sh

    # Create named pipes
    mkfifo /tmp/raw_logs
    mkfifo /tmp/stats
    chmod 666 /tmp/raw_logs /tmp/stats

    # Create user and processor.sh
    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/processor.sh
#!/bin/bash
awk '{
  n++;
  sum += $1;
  sum_sq += $1 * $1;
  mean = sum / n;
  # Naive sum of squared diffs (fails catastrophically for large inputs)
  ssd = sum_sq - (sum * sum)/n;
  printf "%d %.4f %.4f\n", n, mean, ssd;
}'
EOF
    chmod +x /home/user/processor.sh

    # Create supervisor config
    cat << 'EOF' > /etc/supervisor/conf.d/pipeline.conf
[program:log_gen]
command=bash /app/log_gen.sh
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/log_gen-stderr.log
stdout_logfile=/dev/null

[program:processor]
command=bash -c "bash /home/user/processor.sh < /tmp/raw_logs > /tmp/stats"
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/processor-stderr.log
stdout_logfile=/dev/null

[program:log_alert]
command=bash -c "bash /app/log_alert.sh < /tmp/stats >> /home/user/alerts.log"
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/log_alert-stderr.log
stdout_logfile=/dev/null
EOF

    touch /home/user/alerts.log
    chmod -R 777 /home/user