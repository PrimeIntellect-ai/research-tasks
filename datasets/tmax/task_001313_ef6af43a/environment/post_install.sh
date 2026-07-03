apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    mkdir -p /home/user/math_sim
    cd /home/user/math_sim
    git init
    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    cat << 'EOF' > requirements.txt
pytest
EOF

    cat << 'EOF' > sim.py
import math

def run_simulation():
    val = 0.0
    for _ in range(10):
        val += 0.1

    if abs(val - 1.0) < 1e-6:
        return "SUCCESS: 1.0"
    else:
        raise ValueError(f"Divergence detected: {val} != 1.0")

if __name__ == "__main__":
    print(run_simulation())
EOF

    cat << 'EOF' > test_sim.py
from sim import run_simulation

def test_sim():
    assert run_simulation() == "SUCCESS: 1.0"
EOF

    git add requirements.txt sim.py test_sim.py
    git commit -m "Initial working commit"
    git tag v1.0

    # Commit 2: benign
    echo "# Added a comment" >> sim.py
    git commit -am "Add comment"

    # Commit 3: Introduce bug (floating point issue)
    cat << 'EOF' > sim.py
import math

def run_simulation():
    val = 0.0
    for _ in range(10):
        val += 0.1

    # Optimization: exact match is faster
    if val == 1.0:
        return "SUCCESS: 1.0"
    else:
        raise ValueError(f"Divergence detected: {val} != 1.0")

if __name__ == "__main__":
    print(run_simulation())
EOF
    git commit -am "Optimize comparison"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commit 4: Add bad dependency
    cat << 'EOF' > requirements.txt
pytest
nonexistent-math-conflict-package==99.9.9
EOF
    git commit -am "Update dependencies"

    # Commit 5: Add logging
    echo "# Logging enabled" >> sim.py
    git commit -am "Add logging"

    # Store the bad commit hash somewhere for the verification script
    echo $BAD_COMMIT > /tmp/bad_commit_hash

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/math_sim
    chmod -R 777 /home/user
    chmod 777 /tmp/bad_commit_hash