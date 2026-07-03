apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/simulation_repo
    cd /home/user/simulation_repo
    git init
    git config user.name "Test User"
    git config user.email "test@example.com"

    # Commits 1-4
    for i in $(seq 1 4); do
      echo "Setup $i" > README.md
      git add README.md
      git commit -m "chore: setup $i"
    done

    # Commit 5: Secret leak
    echo '{"SIM_SECRET_KEY": "super_secret_physics_99"}' > config.json
    git add config.json
    git commit -m "add config"

    # Commit 6: Remove secret
    git rm config.json
    git commit -m "remove config"

    # Commits 7-9
    for i in $(seq 7 9); do
      echo "Setup $i" > README.md
      git add README.md
      git commit -m "chore: setup $i"
    done

    # Commit 10: Add sim.py (Good state)
    cat << 'EOF' > sim.py
import os
import sys

if os.environ.get("SIM_SECRET_KEY") != "super_secret_physics_99":
    print("Error: Invalid or missing SIM_SECRET_KEY")
    sys.exit(1)

def compute_trajectory(steps):
    pos = 0.0
    for _ in range(steps):
        pos += 0.1
    return pos

if __name__ == "__main__":
    val = compute_trajectory(100)
    if abs(val - 10.0) < 1e-5:
        sys.exit(0)
    else:
        sys.exit(2)
EOF
    git add sim.py
    git commit -m "feat: add physics simulation"
    git tag v1.0

    # Commits 11-150
    for i in $(seq 11 150); do
      echo "Doc update $i" > README.md
      git add README.md
      git commit -m "docs: update $i"
    done

    # Commit 151: Regression (Bad state)
    cat << 'EOF' > sim.py
import os
import sys

if os.environ.get("SIM_SECRET_KEY") != "super_secret_physics_99":
    print("Error: Invalid or missing SIM_SECRET_KEY")
    sys.exit(1)

def compute_trajectory(steps):
    pos = 0.0
    for _ in range(steps):
        pos += 0.1
    return pos

if __name__ == "__main__":
    val = compute_trajectory(100)
    if val == 10.0:
        sys.exit(0)
    else:
        sys.exit(2)
EOF
    git add sim.py
    git commit -m "refactor: simplify precision check"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commits 152-200
    for i in $(seq 152 200); do
      echo "Doc update $i" > README.md
      git add README.md
      git commit -m "docs: update $i"
    done

    # Save the expected ground truths
    echo "super_secret_physics_99" > /tmp/expected_secret.txt
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    chown -R user:user /home/user/simulation_repo
    chmod -R 777 /home/user