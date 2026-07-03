apt-get update && apt-get install -y python3 python3-pip git sqlite3
    pip3 install pytest

    mkdir -p /home/user/app_repo
    mkdir -p /home/user/data

    # 1. Setup Git Repo
    cd /home/user/app_repo
    git init
    git config user.name "SRE"
    git config user.email "sre@example.com"

    cat << 'EOF' > processor.py
def process_metric(name, value):
    print(f"Processing {name}: {value}")
    return True
EOF
    git add processor.py
    git commit -m "Initial commit"
    GOOD_COMMIT=$(git rev-parse HEAD)

    # Add some harmless commits
    for i in {1..3}; do
        echo "# Harmless comment $i" >> processor.py
        git commit -am "Harmless commit $i"
    done

    # Introduce the bug
    cat << 'EOF' > processor.py
def process_metric(name, value):
    print(f"Processing {name}: {value}")
    if value < 0:
        raise ValueError(f"Critical failure: Negative metric value {value} for {name}")
    return True
# Harmless comment 1
# Harmless comment 2
# Harmless comment 3
EOF
    git commit -am "Add metric validation"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Add more harmless commits
    for i in {4..6}; do
        echo "# Harmless comment $i" >> processor.py
        git commit -am "Harmless commit $i"
    done

    # 2. Setup SQLite DB with WAL
    cd /home/user/data
    python3 -c "
import sqlite3
conn = sqlite3.connect('metrics.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.execute('CREATE TABLE metrics (id INTEGER PRIMARY KEY, name TEXT, value REAL)')
conn.execute(\"INSERT INTO metrics (id, name, value) VALUES (1, 'cpu', 45.2)\")
conn.execute(\"INSERT INTO metrics (id, name, value) VALUES (2, 'mem', 80.1)\")
conn.commit()
conn.close()

# Keep connection open to leave WAL behind
conn = sqlite3.connect('metrics.db')
conn.execute(\"INSERT INTO metrics (id, name, value) VALUES (42, 'disk_io', -5.0)\")
conn.commit()
import os
os._exit(0) # Crash without closing to leave WAL intact
"

    # 3. Create Crash Log
    cat << 'EOF' > /home/user/crash.log
Traceback (most recent call last):
  File "worker.py", line 87, in <module>
    main()
  File "worker.py", line 42, in main
    processor.process_metric(metric_name, metric_value)
  File "/home/user/app_repo/processor.py", line 4, in process_metric
    raise ValueError(f"Critical failure: Negative metric value {value} for {name}")
ValueError: Critical failure: Negative metric value -5.0 for disk_io
EOF

    # Save the expected truth values to a hidden file for the verification script
    echo "$BAD_COMMIT" > /tmp/expected_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /tmp/expected_commit.txt