apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create the Python script to generate data
    cat << 'EOF' > /home/user/generate_data.py
import struct
import random
import math

random.seed(42)

# Generate synthetic telemetry data
records = []
num_records = 500000

for _ in range(num_records):
    # Random timestamps spanning 100 seconds (10 buckets)
    ts = random.randint(1000, 1099)

    # 80% chance to be valid, 20% to be outlier distance
    if random.random() < 0.8:
        x = random.uniform(-70.0, 70.0)
        y = random.uniform(-70.0, 70.0)
    else:
        x = random.uniform(80.0, 150.0)
        y = random.uniform(80.0, 150.0)

    val = random.uniform(10.0, 100.0)
    records.append((ts, x, y, val))

# Write binary file
with open('/home/user/telemetry.bin', 'wb') as f:
    for r in records:
        f.write(struct.pack('<ifff', r[0], r[1], r[2], r[3]))

# Compute ground truth
buckets = {}
for ts, x, y, val in records:
    dist = math.sqrt(x*x + y*y)
    if dist <= 100.0:
        b = (ts // 10) * 10
        if b not in buckets:
            buckets[b] = []
        buckets[b].append(val)

sorted_buckets = sorted(buckets.keys())

with open('/home/user/.expected_summary.csv', 'w') as f:
    f.write("bucket,bucket_avg,rolling_avg\n")
    prev_avg = None
    for b in sorted_buckets:
        b_avg = sum(buckets[b]) / len(buckets[b])
        if prev_avg is None:
            r_avg = b_avg
        else:
            r_avg = (b_avg + prev_avg) / 2.0

        f.write(f"{b},{b_avg:.2f},{r_avg:.2f}\n")
        prev_avg = b_avg
EOF

    python3 /home/user/generate_data.py
    rm /home/user/generate_data.py

    chmod -R 777 /home/user