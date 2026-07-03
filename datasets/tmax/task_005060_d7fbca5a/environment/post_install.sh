apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create the setup script to generate raw logs
    cat << 'EOF' > /tmp/setup.py
import os
import random
from datetime import datetime, timedelta

os.makedirs("/home/user/logs/raw", exist_ok=True)

random.seed(42)
start_time = datetime(2023, 10, 24, 0, 0, 0)
endpoints = ["/api/v1/data", "/api/v1/users", "/login", "/checkout"]
ips = [f"192.168.1.{i}" for i in range(10, 50)]

# Baseline response times (mean, std)
baseline = {
    "/api/v1/data": (50, 10),
    "/api/v1/users": (80, 15),
    "/login": (120, 25),
    "/checkout": (200, 40)
}

for server_id in range(1, 21):
    filepath = f"/home/user/logs/raw/server_{server_id:02d}.log"
    with open(filepath, "w") as f:
        for _ in range(500):
            current_time = start_time + timedelta(seconds=random.randint(0, 86400))
            ip = random.choice(ips)
            endpoint = random.choice(endpoints)
            mean, std = baseline[endpoint]

            # 1% chance of anomaly
            if random.random() < 0.01:
                response_time = int(mean + std * random.uniform(3.1, 5.0))
            else:
                response_time = int(random.gauss(mean, std))
                if response_time < 5: response_time = 5

            time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{time_str}] {ip} GET {endpoint} 200 {response_time}\n")
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user