apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user

    # Create the processor.py script
    cat << 'EOF' > /home/user/processor.py
import sys

def process(data):
    if len(data) != 8:
        return "SKIP"
    # Hidden trigger
    if data.lower() == "deadbeef":
        raise ValueError("Fatal parsing error")
    return "OK"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
    try:
        process(sys.argv[1])
        print("Success")
        sys.exit(0)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
EOF
    chmod +x /home/user/processor.py

    # Create the memory dump with some binary garbage and the marker
    python3 -c '
import sys
import random
with open("/home/user/worker.dmp", "wb") as f:
    f.write(bytes([random.randint(0, 255) for _ in range(500)]))
    # Corrupted payload: 1a2b3c4d5e6f7a8b9cdeadbeef0123 with random non-hex chars inserted
    f.write(b"CRIT_PAYLOAD_START:1aX2b3Yc4dZ5e6f7a8b9cdeGadQbeWeXf0123 ")
    f.write(bytes([random.randint(0, 255) for _ in range(500)]))
'

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user