apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/app
    cd /home/user/app
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    # Commit 1: v1.0 (Good) - Thread safe
    cat << 'EOF' > worker.py
import os, sys, threading
if not os.environ.get("CONFIG_PATH"):
    print("Missing config")
    sys.exit(1)
lock = threading.Lock()
def worker():
    for _ in range(100):
        with lock:
            with open("counter.txt", "r") as f: val = int(f.read())
            with open("counter.txt", "w") as f: f.write(str(val + 1))
threads = []
num_threads = int(sys.argv[1]) if len(sys.argv) > 1 else 10
for _ in range(num_threads):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
for t in threads: t.join()
EOF
    git add worker.py
    git commit -m "Initial working version"
    git tag v1.0

    # Commit 2: (Good) - Add logging placeholder
    echo "# added logging initialization" >> worker.py
    git commit -am "Add logging setup"

    # Commit 3: (Bad) - Remove lock, introducing race condition
    cat << 'EOF' > worker.py
import os, sys, threading
if not os.environ.get("CONFIG_PATH"):
    print("Missing config")
    sys.exit(1)
def worker():
    for _ in range(100):
        with open("counter.txt", "r") as f: val = int(f.read())
        with open("counter.txt", "w") as f: f.write(str(val + 1))
threads = []
num_threads = int(sys.argv[1]) if len(sys.argv) > 1 else 10
for _ in range(num_threads):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
for t in threads: t.join()
EOF
    git commit -am "Optimize worker by removing lock bottleneck"

    # Save the bad commit SHA for verification
    git rev-parse HEAD > /home/user/.truth_commit

    # Commit 4: (Bad) - Unrelated change
    echo "# cleaned up unused imports" >> worker.py
    git commit -am "Cleanup imports"

    # Commit 5: (Bad) - HEAD - Minor change
    echo "# updated documentation" >> worker.py
    git commit -am "Update docs"

    chmod -R 777 /home/user