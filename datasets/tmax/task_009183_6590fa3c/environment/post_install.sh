apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

mkdir -p /home/user/sensor_pipeline/data
cd /home/user/sensor_pipeline

git config --global user.email "dev@example.com"
git config --global user.name "Developer"

# Create Python script with naive variance
cat << 'EOF' > process.py
import sys
import csv
import json
import math
import os

def process_file(filepath):
    values = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                values.append(float(row[0]))

    n = len(values)
    if n == 0:
        return 0.0, 0.0

    # Naive variance calculation (susceptible to catastrophic cancellation)
    sum_x = sum(values)
    sum_x2 = sum(x * x for x in values)

    mean = sum_x / n
    variance = (sum_x2 / n) - (mean * mean)

    # This will throw ValueError if variance becomes negative due to float precision
    std_dev = math.sqrt(variance) 

    return mean, variance

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    filepath = sys.argv[1]
    filename = os.path.basename(filepath)
    mean, var = process_file(filepath)

    print(json.dumps({filename: {"mean": mean, "variance": var}}))
EOF

git init
git add process.py
git commit -m "Initial commit: Add naive variance processing"

# Create Welford algorithm commit
cat << 'EOF' > process.py
import sys
import csv
import json
import math
import os

def process_file(filepath):
    values = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                values.append(float(row[0]))

    n = len(values)
    if n == 0:
        return 0.0, 0.0

    # Welford's algorithm for numerical stability
    mean = 0.0
    M2 = 0.0
    for count, x in enumerate(values, 1):
        delta = x - mean
        mean += delta / count
        delta2 = x - mean
        M2 += delta * delta2

    variance = M2 / n
    std_dev = math.sqrt(variance)

    return mean, variance

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    filepath = sys.argv[1]
    filename = os.path.basename(filepath)
    mean, var = process_file(filepath)

    print(json.dumps({filename: {"mean": mean, "variance": var}}))
EOF

git add process.py
git commit -m "Fix variance calculation using Welford's algorithm to prevent precision loss"
WELFORD_COMMIT=$(git rev-parse HEAD)

# Revert Welford algorithm commit
git revert --no-edit $WELFORD_COMMIT

# Add data files and shell script
cat << 'EOF' > data/sensor_A.csv
1.0
2.0
3.0
4.0
5.0
EOF

cat << 'EOF' > "data/sensor B.csv"
10000000000.0
10000000001.0
10000000002.0
EOF

cat << 'EOF' > run_pipeline.sh
#!/bin/bash
# Iterate over all csv files in data directory
for f in $(ls data/*.csv); do
    python3 process.py $f
done
EOF
chmod +x run_pipeline.sh

git add data/ run_pipeline.sh
git commit -m "Add wrapper script and test data"

# Save the target hash for verification
echo "$WELFORD_COMMIT" > /tmp/target_hash.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user/sensor_pipeline
chmod -R 777 /home/user