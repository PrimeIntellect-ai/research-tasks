apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

mkdir -p /home/user/risk_app
cd /home/user/risk_app

git init
git config user.name "OnCall Eng"
git config user.email "oncall@example.com"

# Commit 1: Initial working version
cat << 'EOF' > pipeline.py
import math
import logging

logging.basicConfig(level=logging.INFO)

def compute_risk_score(metrics):
    score = 0.0
    for v in metrics:
        # Avoid log(0)
        score += math.log(v + 1e-9)
    return score

if __name__ == "__main__":
    daily_metrics = [0.5, 0.2, 0.0, 0.8, 0.1]
    logging.info("Starting risk assessment pipeline...")
    final_score = compute_risk_score(daily_metrics)
    print(f"SUCCESS: Pipeline finished. Final Risk Score: {final_score:.4f}")
EOF
git add pipeline.py
git commit -m "Initial working risk pipeline"
WORKING_COMMIT=$(git rev-parse HEAD)

# Commits 2-5: Harmless changes
for i in {2..5}; do
    echo "# Harmless comment $i" >> pipeline.py
    git add pipeline.py
    git commit -m "Add comment $i"
done

# Commit 6: Introduce the numerical bug (remove 1e-9)
cat << 'EOF' > pipeline.py
import math
import logging

logging.basicConfig(level=logging.INFO)

def compute_risk_score(metrics):
    score = 0.0
    for v in metrics:
        # Refactored for cleaner math
        score += math.log(v)
    return score

if __name__ == "__main__":
    daily_metrics = [0.5, 0.2, 0.0, 0.8, 0.1]
    logging.info("Starting risk assessment pipeline...")
    # Harmless comment 2
    # Harmless comment 3
    # Harmless comment 4
    # Harmless comment 5
    final_score = compute_risk_score(daily_metrics)
    print(f"SUCCESS: Pipeline finished. Final Risk Score: {final_score:.4f}")
EOF
git add pipeline.py
git commit -m "Refactor risk score calculation to remove magic numbers"
BAD_COMMIT=$(git rev-parse HEAD)

# Commits 7-10: More harmless changes
for i in {7..10}; do
    echo "# Another harmless comment $i" >> pipeline.py
    git add pipeline.py
    git commit -m "Add another comment $i"
done

# Save the expected bad commit for verification purposes
echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user