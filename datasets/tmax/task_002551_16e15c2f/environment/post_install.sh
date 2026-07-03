apt-get update && apt-get install -y python3 python3-pip openssh-server openssh-client netcat-openbsd espeak curl logrotate
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /app/www
    mkdir -p /home/user/.ssh
    mkdir -p /home/user/Maildir/new

    # Generate audio
    espeak -w /app/incident_voicemail.wav "Hey, we are seeing severe latency spikes. We need you to isolate the metrics for the following three ingress nodes: 192.168.1.50, 10.0.0.12, and 172.16.4.8. Also, if their combined 500-level error rate goes above twelve percent, make sure the system generates an email alert. Thanks."

    # Fake whisper-cli to ensure agent can transcribe if they don't know how to play audio
    cat << 'EOF' > /usr/local/bin/whisper-cli
#!/bin/bash
echo "Hey, we are seeing severe latency spikes. We need you to isolate the metrics for the following three ingress nodes: 192.168.1.50, 10.0.0.12, and 172.16.4.8. Also, if their combined 500-level error rate goes above twelve percent, make sure the system generates an email alert. Thanks."
EOF
    chmod +x /usr/local/bin/whisper-cli

    # Generate ssh keys
    ssh-keygen -t rsa -b 2048 -f /home/user/.ssh/id_rsa -N ""
    cp /home/user/.ssh/id_rsa.pub /home/user/.ssh/authorized_keys

    # Overly permissive permissions to break ssh
    chmod 777 /home/user/.ssh
    chmod 777 /home/user/.ssh/authorized_keys
    chmod 777 /home/user/.ssh/id_rsa

    # Configure custom sshd
    mkdir -p /var/run/sshd
    cat << 'EOF' > /home/user/sshd_config
Port 2222
HostKey /etc/ssh/ssh_host_rsa_key
AuthorizedKeysFile /home/user/.ssh/authorized_keys
StrictModes yes
PasswordAuthentication no
PidFile /home/user/sshd.pid
EOF

    # Generate raw telemetry log and ground truth
    cat << 'EOF' > /tmp/gen.py
import random
from datetime import datetime, timedelta
import csv

ips = ["192.168.1.50", "10.0.0.12", "172.16.4.8", "8.8.8.8", "1.1.1.1"]
start_time = datetime(2023, 10, 1, 0, 0, 0)
log_lines = []
truth = {}

for hour in range(24):
    hour_ts = start_time + timedelta(hours=hour)
    hour_str = hour_ts.strftime('%Y-%m-%d %H:00')
    target_resp = []
    for _ in range(100):
        ip = random.choice(ips)
        status = 200 if random.random() > 0.15 else 500
        resp = random.randint(10, 500)
        ts = hour_ts + timedelta(minutes=random.randint(0, 59))
        log_lines.append((ts, ip, status, resp))
        if ip in ips[:3]:
            target_resp.append(resp)
    if target_resp:
        truth[hour_str] = sum(target_resp) / len(target_resp)

log_lines.sort(key=lambda x: x[0])
with open('/app/www/raw_telemetry.log', 'w') as f:
    for ts, ip, status, resp in log_lines:
        f.write(f"[{ts.strftime('%Y-%m-%d %H:%M:%S')}] {ip} {status} {resp}\n")

with open('/tmp/ground_truth_metrics.csv', 'w') as f:
    for k, v in truth.items():
        f.write(f"{k},{v}\n")
EOF
    python3 /tmp/gen.py

    chown -R user:user /home/user
    chown -R user:user /app
    chmod -R 777 /home/user