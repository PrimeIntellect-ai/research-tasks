apt-get update && apt-get install -y python3 python3-pip git strace
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/malware_analysis
    cd /home/user/malware_analysis
    git init

    # Setup git user
    git config user.email "hacker@malware.com"
    git config user.name "Hacker"

    # Create the hidden file
    python3 -c "
key = 42
plaintext = 'TOP_SECRET_EXFIL_DATA'
encrypted = bytes([ord(c) ^ key for c in plaintext])
with open('/home/user/.hidden_config_xyz_123.dat', 'wb') as f:
    f.write(encrypted)
"

    # Commit 1: Initial working version (No threading, good formula)
    cat << 'EOF' > worker.py
import time

def decrypt_payload(data, key):
    # Correct decryption
    return "".join([chr(b ^ key) for b in data])

def run():
    try:
        with open("/home/user/.hidden_config_xyz_123.dat", "rb") as f:
            data = f.read()
        print(decrypt_payload(data, 42))
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    run()
EOF
    git add worker.py
    git commit -m "Initial commit"
    COMMIT_1=$(git rev-parse HEAD)

    # Commit 2: Some refactoring
    echo "# refactoring" >> worker.py
    git commit -am "Refactor code"

    # Commit 3: Add multi-threading but introduce deadlock
    cat << 'EOF' > worker.py
import time
import threading
import sys

lock1 = threading.Lock()
lock2 = threading.Lock()

def decrypt_payload(data, key):
    return "".join([chr(b ^ key) for b in data])

def worker_a():
    for _ in range(100):
        with lock1:
            time.sleep(0.01)
            with lock2:
                pass

def worker_b():
    for _ in range(100):
        with lock2:
            time.sleep(0.01)
            with lock1:
                pass

def run():
    if "--test-run" in sys.argv:
        t1 = threading.Thread(target=worker_a)
        t2 = threading.Thread(target=worker_b)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        sys.exit(0)

    try:
        with open("/home/user/.hidden_config_xyz_123.dat", "rb") as f:
            data = f.read()
        print(decrypt_payload(data, 42))
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    run()
EOF
    git commit -am "Add multithreading for faster processing"
    DEADLOCK_COMMIT=$(git rev-parse HEAD)

    # Commit 4: Break the decryption formula
    cat << 'EOF' > worker.py
import time
import threading
import sys

lock1 = threading.Lock()
lock2 = threading.Lock()

def decrypt_payload(data, key):
    # Broken decryption (added +1)
    return "".join([chr((b ^ key) + 1) for b in data])

def worker_a():
    for _ in range(100):
        with lock1:
            time.sleep(0.01)
            with lock2:
                pass

def worker_b():
    for _ in range(100):
        with lock2:
            time.sleep(0.01)
            with lock1:
                pass

def run():
    if "--test-run" in sys.argv:
        t1 = threading.Thread(target=worker_a)
        t2 = threading.Thread(target=worker_b)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        sys.exit(0)

    try:
        with open("/home/user/.hidden_config_xyz_123.dat", "rb") as f:
            data = f.read()
        print(decrypt_payload(data, 42))
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    run()
EOF
    git commit -am "Update crypto logic to thwart analysis"

    # Save the target hash to a secure place for verification
    echo "$DEADLOCK_COMMIT" > /tmp/target_hash.txt

    chmod -R 777 /home/user