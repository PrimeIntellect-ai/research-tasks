apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import random
import json

base_dir = "/home/user/sensor_data"
os.makedirs(base_dir, exist_ok=True)

sites = {
    "site_alpha": "csv",
    "site_beta": "jsonl",
    "site_gamma": "csv"
}

# Fix seed for reproducibility
random.seed(42)

valid_temps = []

for site, fmt in sites.items():
    site_dir = os.path.join(base_dir, site)
    os.makedirs(site_dir, exist_ok=True)

    for day in range(1, 4):
        file_path = os.path.join(site_dir, f"2023-05-{day:02d}.{fmt}")
        with open(file_path, "w") as f:
            if fmt == "csv":
                f.write("timestamp,temperature,humidity\n")

            for _ in range(50):
                ts = 1682900000 + random.randint(0, 86400)
                # Introduce occasional invalid records
                if random.random() < 0.05:
                    t = random.uniform(70.0, 100.0) # Invalid temp
                    h = random.uniform(20.0, 80.0)
                elif random.random() < 0.05:
                    t = random.uniform(10.0, 30.0)
                    h = random.uniform(-20.0, -1.0) # Invalid humidity
                else:
                    t = random.uniform(-10.0, 40.0)
                    h = random.uniform(10.0, 90.0)
                    valid_temps.append(t)

                if fmt == "csv":
                    f.write(f"{ts},{t:.2f},{h:.2f}\n")
                else:
                    f.write(json.dumps({"ts": ts, "t": round(t, 2), "h": round(h, 2)}) + "\n")
EOF

    python3 /tmp/setup.py

    cat << 'EOF' > /tmp/golden.py
import os
import glob
import json

base_dir = "/home/user/sensor_data"
valid_t = []

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".csv"):
            with open(os.path.join(root, file), 'r') as f:
                lines = f.readlines()[1:] # skip header
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        t = float(parts[1])
                        h = float(parts[2])
                        if -50.0 <= t <= 60.0 and 0.0 <= h <= 100.0:
                            valid_t.append(t)
        elif file.endswith(".jsonl"):
            with open(os.path.join(root, file), 'r') as f:
                for line in f:
                    data = json.loads(line)
                    t = float(data["t"])
                    h = float(data["h"])
                    if -50.0 <= t <= 60.0 and 0.0 <= h <= 100.0:
                        valid_t.append(t)

max_t = max(valid_t)
min_t = min(valid_t)
avg_t = sum(valid_t) / len(valid_t)

xml_output = f"""<results>
    <metrics>
        <max_temp>{max_t:.2f}</max_temp>
        <min_temp>{min_t:.2f}</min_temp>
        <avg_temp>{avg_t:.2f}</avg_temp>
    </metrics>
</results>"""

# Write truth to a hidden file for test verification
with open("/tmp/golden_results.xml", "w") as f:
    f.write(xml_output)
EOF

    python3 /tmp/golden.py

    chmod -R 777 /home/user