apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/orbital_calc
    cd /home/user/orbital_calc
    git init
    git config user.email "developer@example.com"
    git config user.name "Developer"

    # Create the initial calc.py
    cat << 'EOF' > calc.py
def calculate_apogee(radius):
    return radius * 3.14159265359 + 100.0
EOF
    git add calc.py
    git commit -m "Initial commit: Add apogee calculator"
    git tag v1.0

    # Add 130 good commits
    for i in {1..130}; do
        echo "# chore: minor update $i" >> calc.py
        git commit -am "chore: update $i"
    done

    # BAD COMMIT (Introduces precision loss)
    cat << 'EOF' > calc.py
def calculate_apogee(radius):
    return radius * 3.14 + 100.0
EOF
    git commit -am "refactor: optimize constants for speed"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Add 69 more commits
    for i in {132..200}; do
        echo "# chore: minor update $i" >> calc.py
        git commit -am "chore: update $i"
    done

    # Create the test script (untracked, but present in the working directory)
    mkdir -p tests
    cat << 'EOF' > tests/test_apogee.py
import sys
import math
from calc import calculate_apogee

def test_precision():
    val = calculate_apogee(10.0)
    expected = 10.0 * 3.14159265359 + 100.0
    # Strict tolerance to catch the 3.14 truncation
    if not math.isclose(val, expected, rel_tol=1e-5):
        print(f"Precision error: {val} != {expected}")
        sys.exit(1)
    print("Test passed.")
    sys.exit(0)

if __name__ == "__main__":
    test_precision()
EOF

    # Save the bad commit to a hidden privileged file for test validation
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    chown -R user:user /home/user/orbital_calc
    chmod -R 777 /home/user