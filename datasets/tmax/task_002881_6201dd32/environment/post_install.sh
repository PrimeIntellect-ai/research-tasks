apt-get update && apt-get install -y python3 python3-pip wget jq curl git
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/data
    mkdir -p /app

    # Download yq-3.2.3
    cd /app
    wget -qO v3.2.3.tar.gz https://github.com/kislyuk/yq/archive/refs/tags/v3.2.3.tar.gz
    tar -xzf v3.2.3.tar.gz
    rm v3.2.3.tar.gz

    # Inject broken dependency
    sed -i "s/install_requires=\[/install_requires=\['BROKEN_DEPENDENCY_INJECTED_HERE', /" /app/yq-3.2.3/setup.py

    # Generate data
    cat << 'EOF' > /tmp/gen_data.py
import json
import random
import datetime

random.seed(42)

transactions = []
accounts = [f"ACC-{i:04d}" for i in range(1000)]

def rand_time():
    return datetime.datetime(2023, 1, 1) + datetime.timedelta(days=random.randint(0, 30), minutes=random.randint(0, 1440))

for i in range(10000):
    src = random.choice(accounts)
    dst = random.choice(accounts)
    while dst == src:
        dst = random.choice(accounts)
    transactions.append({
        "tx_id": f"TX-{i}",
        "src_account": src,
        "dst_account": dst,
        "amount": round(random.uniform(10, 1000), 2),
        "timestamp": rand_time().isoformat()
    })

ground_truth = set()
cycle_idx = 10000

# 5 cycles > 50k
for i in range(5):
    a, b, c = random.sample(accounts, 3)
    ground_truth.update([a, b, c])
    amt1 = round(random.uniform(10000, 20000), 2)
    amt2 = round(random.uniform(10000, 20000), 2)
    amt3 = 50001 - amt1 - amt2 + round(random.uniform(1000, 5000), 2)

    transactions.extend([
        {"tx_id": f"TX-{cycle_idx}", "src_account": a, "dst_account": b, "amount": amt1, "timestamp": rand_time().isoformat()},
        {"tx_id": f"TX-{cycle_idx+1}", "src_account": b, "dst_account": c, "amount": amt2, "timestamp": rand_time().isoformat()},
        {"tx_id": f"TX-{cycle_idx+2}", "src_account": c, "dst_account": a, "amount": amt3, "timestamp": rand_time().isoformat()}
    ])
    cycle_idx += 3

# 2 cycles < 50k
for i in range(2):
    a, b, c = random.sample(accounts, 3)
    amt1 = round(random.uniform(1000, 2000), 2)
    amt2 = round(random.uniform(1000, 2000), 2)
    amt3 = round(random.uniform(1000, 2000), 2)

    transactions.extend([
        {"tx_id": f"TX-{cycle_idx}", "src_account": a, "dst_account": b, "amount": amt1, "timestamp": rand_time().isoformat()},
        {"tx_id": f"TX-{cycle_idx+1}", "src_account": b, "dst_account": c, "amount": amt2, "timestamp": rand_time().isoformat()},
        {"tx_id": f"TX-{cycle_idx+2}", "src_account": c, "dst_account": a, "amount": amt3, "timestamp": rand_time().isoformat()}
    ])
    cycle_idx += 3

random.shuffle(transactions)

with open("/home/user/data/transactions.jsonl", "w") as f:
    for t in transactions:
        f.write(json.dumps(t) + "\n")

with open("/tmp/ground_truth.json", "w") as f:
    json.dump(sorted(list(ground_truth)), f)
EOF

    python3 /tmp/gen_data.py
    rm /tmp/gen_data.py

    chmod -R 777 /home/user
    chmod -R 777 /app