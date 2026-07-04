apt-get update && apt-get install -y python3 python3-pip curl build-essential
    pip3 install pytest

    # Install Rust globally so the user can access it
    export RUSTUP_HOME=/opt/rust
    export CARGO_HOME=/opt/rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    chmod -R 777 /opt/rust

    mkdir -p /home/user/data
    cat << 'EOF' > /home/user/data/generate_logs.py
import random

ips = ["192.168.1.15", "10.0.0.4", "172.16.0.8", "192.168.1.100", "10.0.0.99"]
endpoints = ["/api/v1/login", "/api/v1/logout", "/home", "/dashboard", "/settings"]
uagents = ["Mozilla/5.0", "curl/7.68.0", "PostmanRuntime/7.28.4"]
statuses = [200, 404, 500, 401]

random.seed(42)

logs = []
base_time = 1700000000

# Generate exactly 500 unique logs
unique_set = set()
while len(unique_set) < 500:
    ts = base_time + random.randint(0, 3600)
    ip = random.choice(ips)
    ua = random.choice(uagents)
    st = random.choice(statuses)
    ep = random.choice(endpoints)

    tup = (ts, ip, ep)
    if tup not in unique_set:
        unique_set.add(tup)
        logs.append(f"{ts}|{ip}|{ua}|{st}|{ep}\n")

# Inject exactly 150 duplicates (exact tuple matches)
duplicates = random.choices(logs, k=150)
logs.extend(duplicates)

# Shuffle the logs to simulate unordered raw input
random.shuffle(logs)

with open("/home/user/data/raw_logs.txt", "w") as f:
    f.writelines(logs)
EOF
    python3 /home/user/data/generate_logs.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user