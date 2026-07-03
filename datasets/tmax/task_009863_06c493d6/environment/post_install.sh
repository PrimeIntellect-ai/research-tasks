apt-get update && apt-get install -y python3 python3-pip bc gawk time
    pip3 install pytest

    mkdir -p /home/user
    cat << 'EOF' > /home/user/setup_data.py
import csv
import random

random.seed(42)

with open("/home/user/data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["temp", "vibration", "failure"])

    # Generate fail=1
    for i in range(200):
        t = random.randint(70, 79) if i < 50 else random.randint(0, 69)
        v = random.randint(40, 49) if i % 2 == 0 else random.randint(0, 39)
        writer.writerow([t, v, 1])

    # Generate fail=0
    for i in range(800):
        t = random.randint(70, 79) if i < 40 else random.randint(0, 69)
        v = random.randint(40, 49) if i % 10 == 0 else random.randint(0, 39)
        writer.writerow([t, v, 0])
EOF
    python3 /home/user/setup_data.py
    rm /home/user/setup_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user