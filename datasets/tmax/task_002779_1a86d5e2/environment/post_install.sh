apt-get update && apt-get install -y python3 python3-pip build-essential wget tar
    pip3 install pytest

    # Create user
    useradd -m -s /bin/bash user || true

    # Download and set up dos2unix-7.4.3
    mkdir -p /app
    cd /app
    wget https://sourceforge.net/projects/dos2unix/files/dos2unix/7.4.3/dos2unix-7.4.3.tar.gz
    tar -xzf dos2unix-7.4.3.tar.gz
    rm dos2unix-7.4.3.tar.gz
    cd dos2unix-7.4.3
    sed -i '45i LDFLAGS_EXTRA = -lnonexistent_lib' Makefile

    # Generate data and golden reference
    mkdir -p /golden
    python3 -c '
import random
import os

timestamps = [
    ("[14:05:01]", "14:05:01"),
    ("14:05:01 PM", "14:05:01"),
    ("T14:05:01Z", "14:05:01"),
    ("[09:12:34]", "09:12:34"),
    ("09:12:34 AM", "09:12:34"),
    ("T09:12:34Z", "09:12:34")
]

texts = [
    ("Hello, world!", "hello world"),
    ("  How are you?  ", "how are you"),
    ("Wait... what?!", "wait what"),
    ("This is a test.", "this is a test")
]

raw_lines = []
golden_lines = []

for _ in range(1000):
    ts_raw, ts_clean = random.choice(timestamps)
    txt_raw, txt_clean = random.choice(texts)

    raw_lines.append(f"{ts_raw} {txt_raw}\r\n")
    golden_lines.append(f"{ts_clean}\t{txt_clean}\n")

with open("/home/user/raw_subs.txt", "wb") as f:
    for line in raw_lines:
        f.write(line.encode("utf-8"))

with open("/golden/reference.tsv", "w", encoding="utf-8") as f:
    for line in golden_lines:
        f.write(line)
'

    # Create verifier script
    cat << 'EOF' > /verify_metric.py
import sys

def verify():
    try:
        with open("/home/user/normalized_subs.tsv", "r") as f:
            agent_lines = f.readlines()
    except FileNotFoundError:
        print("normalized_subs.tsv not found.")
        sys.exit(1)

    with open("/golden/reference.tsv", "r") as f:
        golden_lines = f.readlines()

    score = len(set(agent_lines) & set(golden_lines)) / len(set(golden_lines))
    print(f"Score: {score}")
    if score >= 0.90:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    verify()
EOF

    chmod +x /verify_metric.py
    chmod -R 777 /home/user