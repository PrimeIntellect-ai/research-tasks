apt-get update && apt-get install -y python3 python3-pip redis-server openssh-server curl cron
    pip3 install pytest flask redis

    # Create user
    useradd -m -s /bin/bash user || true

    # Create directories
    mkdir -p /app/logs /app/sshd /home/user/.ssh

    # Create heartbeat log
    cat << 'EOF' > /app/logs/heartbeat.log
[1710000000] frontend HEARTBEAT_OK
[1710000010] backend HEARTBEAT_FAIL
[1710000020] frontend HEARTBEAT_OK
EOF

    # Create monitor_sync.sh
    cat << 'EOF' > /home/user/monitor_sync.sh
#!/bin/bash
scp -P 2222 -i /home/user/.ssh/monitor_key -o StrictHostKeyChecking=no user@127.0.0.1:/app/logs/heartbeat.log /tmp/heartbeat.log
cat /tmp/heartbeat.log | python3 /home/user/log_parser.py > /tmp/parsed.csv
curl -X POST --data-binary @/tmp/parsed.csv http://127.0.0.1:5000/submit
EOF
    chmod +x /home/user/monitor_sync.sh

    # Create SSH keys
    ssh-keygen -t rsa -b 2048 -f /home/user/.ssh/monitor_key -N ""
    cp /home/user/.ssh/monitor_key.pub /app/sshd/authorized_keys

    # Create sshd_config
    cat << 'EOF' > /app/sshd/sshd_config
Port 2222
HostKey /etc/ssh/ssh_host_rsa_key
AuthorizedKeysFile /app/sshd/authorized_keys
StrictModes no
PidFile /tmp/sshd.pid
EOF

    # Create Flask Aggregator
    cat << 'EOF' > /app/flask_aggregator.py
from flask import Flask, request
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_data()
    r.set('latest_metrics', data)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    # Create Oracle Parser
    cat << 'EOF' > /app/oracle_parser
#!/usr/bin/env python3
import sys
import csv

def parse_logs():
    services = {}
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 3:
            continue
        ts_str, svc, event = parts
        if not (ts_str.startswith('[') and ts_str.endswith(']')):
            continue
        try:
            ts = int(ts_str[1:-1])
        except ValueError:
            continue

        if event not in ('HEARTBEAT_OK', 'HEARTBEAT_FAIL'):
            continue

        if svc not in services:
            services[svc] = {'last_ts': -1, 'ok': 0, 'fail': 0, 'max_ok': 0, 'curr_ok': 0}

        if ts < services[svc]['last_ts']:
            continue

        services[svc]['last_ts'] = ts

        if event == 'HEARTBEAT_OK':
            services[svc]['ok'] += 1
            services[svc]['curr_ok'] += 1
            if services[svc]['curr_ok'] > services[svc]['max_ok']:
                services[svc]['max_ok'] = services[svc]['curr_ok']
        else:
            services[svc]['fail'] += 1
            services[svc]['curr_ok'] = 0

    writer = csv.writer(sys.stdout)
    writer.writerow(['SERVICE_NAME', 'TOTAL_OK', 'TOTAL_FAIL', 'MAX_CONSECUTIVE_OK'])
    for svc in sorted(services.keys()):
        s = services[svc]
        writer.writerow([svc, s['ok'], s['fail'], s['max_ok']])

if __name__ == '__main__':
    parse_logs()
EOF
    chmod +x /app/oracle_parser

    # Ensure ssh host keys exist
    ssh-keygen -A
    mkdir -p /run/sshd

    chown -R user:user /app/sshd
    chmod 600 /app/sshd/authorized_keys

    chmod -R 777 /home/user
    chmod 644 /home/user/.ssh/monitor_key