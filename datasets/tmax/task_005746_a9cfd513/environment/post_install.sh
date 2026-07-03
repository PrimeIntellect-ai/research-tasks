apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        cargo \
        rustc \
        gawk \
        sed \
        grep \
        tar \
        gzip \
        coreutils

    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/storage_dump
    cd /home/user/storage_dump

    cat << 'EOF' > generate_logs.py
import random

nodes = ["NODE_10", "NODE_42", "NODE_77", "NODE_99"]
levels = ["INFO", "WARN", "DEBUG"]
msgs = ["Health check passed", "Process killed", "Spike detected", "Normal operation"]

with open("sys_01.log", "w") as f1, open("sys_02.log", "w") as f2:
    ts = 1710000000
    for i in range(2000):
        ts += random.randint(1, 100)
        node = random.choice(nodes)
        cpu = random.randint(1, 99)
        ram = random.randint(1024, 65536)
        disk = random.randint(100, 2000)
        msg = random.choice(msgs)
        line = f"[{ts}] [{random.choice(levels)}] [{node}] - CPU: {cpu}% RAM: {ram}MB DISK: {disk}GB MSG: {msg}\n"

        if i % 2 == 0:
            f1.write(line)
        else:
            f2.write(line)

    f1.write("[1710009999] [INFO] [NODE_42] - CPU: 12% RAM: 4096MB DISK: 250GB MSG: Sync\n")
    f2.write("[1710010005] [WARN] [NODE_42] - CPU: 99% RAM: 65536MB DISK: 1900GB MSG: Heavy load\n")
EOF

    python3 generate_logs.py
    rm generate_logs.py

    tar -czf metrics_backup.tar.gz sys_01.log sys_02.log
    split -b 50K metrics_backup.tar.gz metrics_backup.tar.gz.
    rm sys_01.log sys_02.log metrics_backup.tar.gz

    chown -R user:user /home/user
    chmod -R 777 /home/user