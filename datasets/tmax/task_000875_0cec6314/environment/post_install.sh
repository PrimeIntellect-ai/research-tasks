apt-get update && apt-get install -y python3 python3-pip strace
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/log_processor.py
import sys
import threading
import time

def process_log(line):
    line = line.strip()
    if "CRITICAL_RACE_CONDITION_883" in line:
        # Induce a deadlock by double-acquiring a non-reentrant lock
        lock = threading.Lock()
        lock.acquire()
        lock.acquire() # Deadlocks here, translates to a futex wait in Linux
    else:
        time.sleep(0.01)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: log_processor.py <logfile>")
        sys.exit(1)

    threads = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            t = threading.Thread(target=process_log, args=(line,))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()
EOF

    cat << 'EOF' > /home/user/incoming_logs.txt
INFO: Starting synchronization task
WARN: Latency spike detected on eth0
INFO: User 459 authenticated successfully
DEBUG: Parsing request payload
INFO: CRITICAL_RACE_CONDITION_883 in module auth_service
WARN: Disk space running low on /var/log
INFO: Shutting down background workers
EOF

    chmod +x /home/user/log_processor.py
    chmod 644 /home/user/incoming_logs.txt

    chmod -R 777 /home/user