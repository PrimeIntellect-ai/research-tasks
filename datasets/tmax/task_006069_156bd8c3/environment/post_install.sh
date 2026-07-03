apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/math_repo
    cd /home/user/math_repo
    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    # Initial working sim.py
    cat << 'EOF' > sim.py
import sys
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=1)
args = parser.parse_args()

random.seed(args.seed)
val = random.randint(1, 1000000)
print(f"Simulation result: {val * 3.14159}")
sys.exit(0)
EOF

    git add sim.py
    git commit -m "Initial commit: math simulation"

    # Create some clean history
    for i in {1..20}; do
        echo "# Change $i" >> sim.py
        git commit -am "Minor simulation tweak $i"
    done

    # Tag v1.0
    git tag v1.0

    # More history
    for i in {21..45}; do
        echo "# Change $i" >> sim.py
        git commit -am "Minor simulation tweak $i"
    done

    # Add the secret seed
    echo "849302" > debug_seed.txt
    git add debug_seed.txt
    git commit -m "Add debug seed for intermittent failing case"

    # Delete the secret seed
    git rm debug_seed.txt
    git commit -m "Clean up debug files"

    # More history
    for i in {46..120}; do
        echo "# Change $i" >> sim.py
        git commit -am "Minor simulation tweak $i"
    done

    # Introduce the regression
    cat << 'EOF' > sim.py
import sys
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=1)
args = parser.parse_args()

random.seed(args.seed)
val = random.randint(1, 1000000)

# Regression introduced here
if args.seed == 849302:
    print("ZeroDivisionError: matrix inversion failed")
    sys.exit(1)

print(f"Simulation result: {val * 3.14159}")
sys.exit(0)
EOF
    git commit -am "Refactor matrix transformation logic"
    BAD_COMMIT=$(git rev-parse HEAD)

    # More history to bury the regression
    for i in {121..180}; do
        echo "# Change $i" >> sim.py
        git commit -am "Minor simulation tweak $i"
    done

    # Save the bad commit to a protected location so the test can verify it
    mkdir -p /tmp/truth
    echo "$BAD_COMMIT" > /tmp/truth/expected_bad_commit.txt

    chmod -R 777 /home/user