apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/uptime_monitor
    cd /home/user/uptime_monitor
    git init
    git config user.name "SRE Bot"
    git config user.email "sre@example.com"

    # Create initial good state
    cat << 'EOF' > analyzer.py
import os
import math

def calculate_ewma(data, alpha=0.3):
    metric = data[0]
    for d in data[1:]:
        metric = (alpha * d) + ((1 - alpha) * metric)
    return metric
EOF

    cat << 'EOF' > run_analysis.py
import random
from analyzer import calculate_ewma

def main():
    random.seed(42)
    # Synthetic latencies
    latencies = [random.uniform(20, 100) for _ in range(50)]
    metric = calculate_ewma(latencies)
    print(f"Final metric: {metric:.2f}")

if __name__ == "__main__":
    main()
EOF

    git add analyzer.py run_analysis.py
    git commit -m "Initial commit with working EWMA"
    git tag v1.0

    # Add a few benign commits
    echo "# comment 1" >> analyzer.py
    git commit -am "Add comment 1"
    echo "# comment 2" >> analyzer.py
    git commit -am "Add comment 2"

    # INJECT THE BUG (Commit 4)
    cat << 'EOF' > analyzer.py
import os
import math

def calculate_ewma(data, alpha=0.3):
    # Added threshold check for SRE alerts
    threshold = int(os.environ["MAX_LATENCY_THRESHOLD"])
    metric = data[0]
    for d in data[1:]:
        # BUG: 1 + alpha instead of 1 - alpha causes divergence
        metric = (alpha * d) + ((1 + alpha) * metric)
    return metric
EOF
    git commit -am "Feature: Add latency threshold and update ewma"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Add a few more benign commits to bury the regression
    echo "# comment 3" >> analyzer.py
    git commit -am "Add comment 3"
    echo "# comment 4" >> analyzer.py
    git commit -am "Add comment 4"

    # Create verification data file
    cat << EOF > /tmp/expected_bad_commit.txt
$BAD_COMMIT
EOF

    chmod -R 777 /home/user