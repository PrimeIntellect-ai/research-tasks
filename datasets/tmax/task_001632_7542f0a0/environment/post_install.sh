apt-get update && apt-get install -y python3 python3-pip gawk coreutils
    pip3 install pytest

    mkdir -p /home/user
    cat << 'EOF' > /home/user/generate_data.py
import random
from datetime import datetime, timedelta

random.seed(42)
servers = [f"srv{i:02d}" for i in range(1, 11)]
keys = [
    "/etc/nginx/nginx.conf",
    "/etc/ssh/sshd_config",
    "/etc/mysql/my.cnf",
    "/etc/redis/redis.conf",
    "/etc/systemd/system.conf"
]

events = []
base_time = datetime(2023, 10, 1, 0, 0, 0)

for i in range(1000):
    dt = base_time + timedelta(minutes=random.randint(1, 10000))
    srv = random.choice(servers)
    key = random.choice(keys)
    added = random.randint(0, 500)
    removed = random.randint(0, 500)
    events.append((dt, srv, key, added, removed))

# Shuffle completely to ensure the agent must sort it
random.shuffle(events)

with open("/home/user/config_events.log", "w") as f:
    for e in events:
        f.write(f"{e[0].isoformat()}|{e[1]}|{e[2]}|{e[3]}|{e[4]}\n")
EOF
    python3 /home/user/generate_data.py
    rm /home/user/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user