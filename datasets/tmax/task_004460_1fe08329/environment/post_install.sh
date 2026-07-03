apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/service
    cd /home/user/service

    # 1. Create the core dump
    printf "\x00\x14\x55\x88\x99Some binary garbage here...\x00\x00LAST_USER_ID=U847291\x00\x00\x11More garbage" > core.dump

    # 2. Create the payload file
    rm -f payload_large.dat
    for i in $(seq 1 100); do
        if [ $i -eq 42 ]; then
            echo "PAYLOAD_DATA:8F:BAD_DATA" >> payload_large.dat
        else
            echo "PAYLOAD_DATA:0$((i%9)):OK_DATA" >> payload_large.dat
        fi
    done

    # 3. Setup git repo
    git init
    git config user.email "oncall@example.com"
    git config user.name "On Call"

    cat << 'EOF' > test_runner.py
import sys

def process_payload(line):
    parts = line.strip().split(':')
    if len(parts) < 2: return True
    hex_val = parts[1]

    # Bug: using signed byte parsing in the bad commit
    val = int(hex_val, 16)
    return parse_val(val)

def parse_val(val):
    # GOOD VERSION
    return True

if __name__ == "__main__":
    try:
        with open("payload_large.dat", "r") as f:
            for line in f:
                process_payload(line)
        sys.exit(0)
    except Exception as e:
        sys.exit(1)
EOF

    git add test_runner.py
    git commit -m "Initial commit"
    git branch -M main

    # Create 10 good commits
    for i in $(seq 1 10); do
        echo "# Comment $i" >> test_runner.py
        git commit -am "Good commit $i"
    done

    # Bad commit (Commit 12)
    cat << 'EOF' > test_runner.py
import sys
import struct

def process_payload(line):
    parts = line.strip().split(':')
    if len(parts) < 2: return True
    hex_val = parts[1]

    val = int(hex_val, 16)
    return parse_val(val)

def parse_val(val):
    # BAD VERSION: assumes values are 0-127. High bit triggers unpack error.
    packed = struct.pack('B', val)
    unpacked = struct.unpack('b', packed)[0] # Will fail for >127
    if unpacked < 0:
        raise ValueError("Signed integer overflow detected!")
    return True

if __name__ == "__main__":
    try:
        with open("payload_large.dat", "r") as f:
            for line in f:
                process_payload(line)
        sys.exit(0)
    except Exception as e:
        sys.exit(1)
EOF
    git commit -am "Refactor payload parsing"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Create 5 more bad commits
    for i in $(seq 1 5); do
        echo "# Extra comment $i" >> test_runner.py
        git commit -am "Another commit $i"
    done

    # Save expected truth values locally for test runner
    echo "U847291" > /home/user/expected_userid.txt
    echo "$BAD_COMMIT" > /home/user/expected_commit.txt
    echo "PAYLOAD_DATA:8F:BAD_DATA" > /home/user/expected_payload.txt

    chmod -R 777 /home/user