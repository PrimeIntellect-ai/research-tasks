apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    mkdir -p /home/user/metric_service
    cd /home/user/metric_service
    git init
    git config user.email "it@company.com"
    git config user.name "IT Setup"

    # Commit 1 (Good)
    cat << 'EOF' > calc.py
def calc_health(uptime, latency):
    return (0.8 * uptime) + (200.0 / latency)

def run():
    states = []
    for u, l in [(99.9, 50), (95.0, 100), (99.0, 20)]:
        states.append(calc_health(u, l))
    print(f"Final Average: {sum(states)/len(states):.2f}")

if __name__ == "__main__":
    run()
EOF
    git add calc.py
    git commit -m "Initial working metric calculation"

    # Commit 2 (Formatting)
    cat << 'EOF' > calc.py
def calc_health(uptime, latency):
    # Calculate weighted health
    return (0.8 * uptime) + (200.0 / latency)

def run():
    states = []
    # Loop over static test data
    for u, l in [(99.9, 50), (95.0, 100), (99.0, 20)]:
        states.append(calc_health(u, l))
    print(f"Final Average: {sum(states)/len(states):.2f}")

if __name__ == "__main__":
    run()
EOF
    git add calc.py
    git commit -m "Add comments to calc.py"

    # Commit 3 (Bad - Introduces formula error)
    cat << 'EOF' > calc.py
def calc_health(uptime, latency):
    # Calculate weighted health
    return (0.8 * uptime) - (200.0 / latency)

def run():
    states = []
    # Loop over static test data
    for u, l in [(99.9, 50), (95.0, 100), (99.0, 20)]:
        states.append(calc_health(u, l))
    print(f"Final Average: {sum(states)/len(states):.2f}")

if __name__ == "__main__":
    run()
EOF
    git add calc.py
    git commit -m "Optimize metric formula"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commit 4 (Unrelated)
    cat << 'EOF' > README.md
# Metric Service
Runs background health calculations.
EOF
    git add README.md
    git commit -m "Add README"

    # Save the bad commit hash somewhere the verifier can read it (hidden from agent)
    echo $BAD_COMMIT > /tmp/.bad_commit_hash

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user