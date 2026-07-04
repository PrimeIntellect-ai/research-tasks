apt-get update && apt-get install -y python3 python3-pip procps
pip3 install pytest

useradd -m -s /bin/bash user || true

cat << 'EOF' > /home/user/.env
export LOG_LEVEL="INFO"
export MAX_RETRIES="O"
export ALERT_EMAIL="devops@local"
EOF

cat << 'EOF' > /home/user/generate_logs.py
import random
random.seed(42)
with open('/home/user/app.log', 'w') as f:
    for i in range(1, 1001):
        if i == 734:
            f.write(f"2023-10-27 10:15:30 [ERROR] CRITICAL_FAILURE_DB_CONNECTION_DROPPED\n")
        else:
            f.write(f"2023-10-27 10:15:30 [INFO] Processed request {i} successfully.\n")
EOF

cat << 'EOF' > /home/user/process_logs.sh
#!/bin/bash

source /home/user/.env

INPUT_FILE=$1
REPORT_FILE="/home/user/report.txt"

info_count=0
critical_count=0

while IFS= read -r line; do
    if [[ "$line" == *"[INFO]"* ]]; then
        ((info_count++))
    elif [[ "$line" == *"[ERROR] CRITICAL"* ]]; then
        # This will fail because MAX_RETRIES is "O" instead of "0"
        (( retries = MAX_RETRIES + 1 ))
        ((critical_count++))
        echo "Handled critical error, retry $retries" > /dev/null
    fi
done < "$INPUT_FILE"

echo "INFO_COUNT=$info_count" > "$REPORT_FILE"
echo "CRITICAL_COUNT=$critical_count" >> "$REPORT_FILE"
echo "SUCCESS" >> "$REPORT_FILE"
EOF
chmod +x /home/user/process_logs.sh

cat << 'EOF' > /.singularity.d/env/99-setup.sh
if ! pgrep -f "tail -f /home/user/app.log" > /dev/null; then
    python3 /home/user/generate_logs.py
    tail -f /home/user/app.log > /dev/null 2>&1 &
    sleep 0.1
    rm -f /home/user/app.log
fi
EOF

chmod -R 777 /home/user