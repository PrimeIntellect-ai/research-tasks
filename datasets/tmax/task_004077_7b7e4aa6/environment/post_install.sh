apt-get update && apt-get install -y python3 python3-pip curl tar
    pip3 install pytest

    mkdir -p /home/user/data
    mkdir -p /home/user/vendor

    # Download and vendor networkx 3.1
    curl -sSL https://github.com/networkx/networkx/archive/refs/tags/networkx-3.1.tar.gz | tar -xz -C /home/user/vendor
    mv /home/user/vendor/networkx-networkx-3.1 /home/user/vendor/networkx

    # Inject perturbation
    sed -i '/def simple_cycles(/a \    return iter([])' /home/user/vendor/networkx/networkx/algorithms/cycles.py

    # Generate data and ground truth
    python3 -c '
import csv, json, os

os.makedirs("/home/user/data", exist_ok=True)

held = [
    ("T1", "R1"),
    ("T2", "R2"),
    ("T3", "R3"),
    ("T4", "R4"),
    ("T5", "R5"),
    ("T6", "R6")
]

req = [
    ("T1", "R2"),
    ("T2", "R3"),
    ("T3", "R1"),
    ("T4", "R5"),
    ("T5", "R4"),
    ("T6", "R1")
]

with open("/home/user/data/held_locks.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["txn_id", "resource_id"])
    writer.writerows(held)

with open("/home/user/data/requested_locks.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["txn_id", "resource_id"])
    writer.writerows(req)

cycles = [["T1", "T2", "T3"], ["T4", "T5"]]
with open("/tmp/ground_truth.json", "w") as f:
    json.dump(cycles, f)
'

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user