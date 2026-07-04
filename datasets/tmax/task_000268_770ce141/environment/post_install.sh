apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    python3 -c '
import os
import random

base_dir = "/home/user/storage_pool"
os.makedirs(base_dir, exist_ok=True)

levels = ["INFO", "WARN", "ERROR"]
users = ["admin", "sysop", "guest", "db_svc"]
actions = ["login", "query", "backup", "restart", "upload"]
statuses = ["success", "failed", "pending", "timeout"]

# Generate dummy vlog files
for d in range(5):
    dir_path = os.path.join(base_dir, f"node_{d}", f"service_{d}")
    os.makedirs(dir_path, exist_ok=True)

    for f in range(10):
        file_path = os.path.join(dir_path, f"log_{f}.vlog")
        lines_count = random.randint(10, 50)

        with open(file_path, "w") as out:
            for l in range(lines_count):
                lvl = random.choice(levels)
                user = random.choice(users)
                act = random.choice(actions)
                stat = random.choice(statuses)
                out.write(f"[{lvl}] 2023-10-01 12:00:00 - User: {user} - Action: {act} - Status: {stat}\n")

        # Lock 20% of the files
        if random.random() < 0.2:
            with open(file_path + ".lock", "w") as lock_out:
                lock_out.write("LOCKED")
'

    chmod -R 777 /home/user