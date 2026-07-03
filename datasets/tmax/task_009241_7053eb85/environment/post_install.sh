apt-get update && apt-get install -y python3 python3-pip procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/simulated_service

    cat << 'EOF' > /home/user/simulated_service/check_db.py
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--user')
parser.add_argument('--password')
args = parser.parse_args()

# Simulate quick execution
time.sleep(0.2)
EOF

    cat << 'EOF' > /home/user/simulated_service/runner.sh
#!/bin/bash
while true; do
    python3 /home/user/simulated_service/check_db.py --host 127.0.0.1 --user admin --password "P@ssw0rd_L3ak_77#!" > /dev/null 2>&1 &
    sleep 1.5
done
EOF

    chmod +x /home/user/simulated_service/check_db.py
    chmod +x /home/user/simulated_service/runner.sh

    chmod -R 777 /home/user