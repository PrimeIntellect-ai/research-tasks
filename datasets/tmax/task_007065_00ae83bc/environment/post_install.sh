apt-get update && apt-get install -y python3 python3-pip gdb coreutils
    pip3 install pytest

    mkdir -p /home/user/worker_node
    cd /home/user/worker_node

    # Generate a random 16-char token
    TOKEN=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)
    echo -n "STUCK_JOB_ID_${TOKEN}" > /home/user/worker_node/.secret_token

    # Create the buggy processor.py
    cat << 'EOF' > /home/user/worker_node/processor.py
import threading
import time
import sys
import os

lock_a = threading.Lock()
lock_b = threading.Lock()

def process_stage_1(job_data):
    with lock_a:
        time.sleep(0.01) # Simulate work and widen race window
        with lock_b:
            pass

def process_stage_2(job_data):
    with lock_b:
        time.sleep(0.01) # Simulate work and widen race window
        with lock_a:
            pass

def worker_thread(mode):
    # Load secret token into memory specifically for the buggy run
    try:
        with open("/home/user/worker_node/.secret_token", "r") as f:
            active_job_id = f.read().strip()
    except Exception:
        active_job_id = "STUCK_JOB_ID_MISSING"

    if mode == 1:
        process_stage_1(active_job_id)
    else:
        process_stage_2(active_job_id)

def main():
    threads = []
    # Create enough threads to guarantee a deadlock under concurrent scheduling
    for i in range(50):
        t1 = threading.Thread(target=worker_thread, args=(1,))
        t2 = threading.Thread(target=worker_thread, args=(2,))
        threads.extend([t1, t2])

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user