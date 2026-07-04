apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    mkdir -p /home/user/logs
    mkdir -p /home/user/anomaly_detector

    # Create input data
    cat << 'EOF' > /home/user/data.csv
metric_id,value
server_1,2.0
server_2,3.0
server_3,10.0
server_4,16.0
EOF

    # Create the cron log indicating the failure
    cat << 'EOF' > /home/user/logs/cron_error.log
[2023-10-27 03:00:01] INFO: Starting anomaly detection pipeline...
[2023-10-27 03:00:01] INFO: Loading data from /home/user/data.csv
Traceback (most recent call last):
  File "/home/user/anomaly_detector/detector.py", line 45, in <module>
    main()
  File "/home/user/anomaly_detector/detector.py", line 40, in main
    processed = compute_baseline(val)
  File "/home/user/anomaly_detector/detector.py", line 22, in compute_baseline
    raise ValueError(f"Convergence failure for value {val}. Max iterations reached.")
ValueError: Convergence failure for value 2.0. Max iterations reached.
EOF

    # Initialize Git repository
    cd /home/user/anomaly_detector
    git init
    git config user.name "OnCall Admin"
    git config user.email "admin@example.com"

    # Create initial python script (Good state)
    cat << 'EOF' > detector.py
import argparse
import csv

def compute_baseline(val):
    # Iterative method to compute square root for baseline
    x = val
    epsilon = 1e-7
    for _ in range(1000):
        next_x = 0.5 * (x + val / x)
        if abs(next_x - x) < epsilon:
            return next_x
        x = next_x
    raise ValueError(f"Convergence failure for value {val}. Max iterations reached.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    results = []
    with open(args.input, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = float(row['value'])
            res = compute_baseline(val)
            results.append({'metric_id': row['metric_id'], 'baseline': res})

    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['metric_id', 'baseline'])
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()
EOF

    git add detector.py
    git commit -m "Initial commit: Add baseline detector"

    # Commit 2 (Good)
    echo "# Added some comments" >> detector.py
    git commit -am "Docs: Update comments"

    # Commit 3 (Good)
    sed -i 's/import csv/import csv\nimport sys/g' detector.py
    git commit -am "Refactor: Add sys import"

    # Commit 4 (Bad) - Introduces the floating point / convergence bug
    sed -i 's/epsilon = 1e-7/epsilon = 1e-17/g' detector.py
    git commit -am "Tune: Increase precision of baseline computation"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commit 5 (Bad - inherited)
    sed -i 's/import sys/import sys\nimport os/g' detector.py
    git commit -am "Refactor: Add os import"

    # Commit 6 (Bad - inherited)
    echo "# End of file" >> detector.py
    git commit -am "Docs: Add EOF comment"

    # Save the bad commit hash to a secret location for verification
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod 777 /tmp/expected_bad_commit.txt