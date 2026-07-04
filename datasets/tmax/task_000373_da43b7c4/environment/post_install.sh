apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/sim_repo
    cd /home/user/sim_repo
    git init

    cat << 'EOF' > simulate.py
import math
import sys
import struct

def dump_memory():
    with open("sim_memory.dmp", "wb") as f:
        f.write(b'\x00' * 1024)
        f.write(b'GARBAGE_DATA_12345\x01\x02\x03')
        f.write(b'ERR_CODE_FP_CANCELLATION_9921')
        f.write(b'\x00' * 512)

def calculate_energy(x):
    # GOOD VERSION
    return 1.0 / (math.sqrt(x**2 + 1) + x)

def run_simulation():
    try:
        val = 0
        for i in range(1, 10):
            x = 10**i
            energy = calculate_energy(x)
            val += 1.0 / energy
        print("Simulation success. Final value:", val)
    except Exception as e:
        dump_memory()
        sys.exit(1)

if __name__ == "__main__":
    run_simulation()
EOF

    git add simulate.py
    git config user.email "aris@example.com"
    git config user.name "Aris"
    git commit -m "Initial commit: working simulation"

    # Add a few good commits
    for i in {1..3}; do
        echo "# comment $i" >> simulate.py
        git commit -am "Minor update $i"
    done

    # Introduce the bad commit
    cat << 'EOF' > simulate.py
import math
import sys
import struct

def dump_memory():
    with open("sim_memory.dmp", "wb") as f:
        f.write(b'\x00' * 1024)
        f.write(b'GARBAGE_DATA_12345\x01\x02\x03')
        f.write(b'ERR_CODE_FP_CANCELLATION_9921')
        f.write(b'\x00' * 512)

def calculate_energy(x):
    # BAD VERSION: Catastrophic cancellation
    return math.sqrt(x**2 + 1) - x

def run_simulation():
    try:
        val = 0
        for i in range(1, 10):
            x = 10**i
            energy = calculate_energy(x)
            val += 1.0 / energy
        print("Simulation success. Final value:", val)
    except Exception as e:
        dump_memory()
        sys.exit(1)

if __name__ == "__main__":
    run_simulation()
EOF

    git commit -am "Refactor energy calculation"
    BAD_COMMIT=$(git rev-parse HEAD)
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    # Add a few more commits so HEAD is not the exact bad commit
    for i in {4..6}; do
        echo "# another comment $i" >> simulate.py
        git commit -am "More updates $i"
    done

    chown -R user:user /home/user/sim_repo
    chmod -R 777 /home/user