apt-get update && apt-get install -y python3 python3-pip sqlite3
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/logs /home/user/app

    # 1. Create fragmented logs
    cat << 'EOF' > /home/user/logs/web.log
[2023-10-24 10:00:01] INFO Incoming request
[2023-10-24 10:00:05] WARN Slow response
EOF

    cat << 'EOF' > /home/user/logs/worker.log
10:00:02 2023-10-24 | INFO | Processing job
10:00:06 2023-10-24 | ERROR | Connection timed out
EOF

    cat << 'EOF' > /home/user/logs/db.log
2023/10/24-10:00:03 - INFO - Query executed
2023/10/24-10:00:07 - FATAL - Out of memory: CRASH_ID_883
EOF

    # 2. Create SQLite DB and leave WAL uncommitted
    python3 -c "
import sqlite3
import os
conn = sqlite3.connect('/home/user/app/data.db', isolation_level=None)
conn.execute('PRAGMA journal_mode=WAL')
conn.execute('CREATE TABLE transactions (id INTEGER, secret_token TEXT)')
conn.execute('INSERT INTO transactions VALUES (1, \"REC_OLD_001\")')
conn.execute('BEGIN TRANSACTION')
conn.execute('INSERT INTO transactions VALUES (2, \"REC_NEW_774\")')
conn.commit()
# Exit immediately to avoid clean checkpoint
os._exit(0)
"

    # 3. Create vulnerable server script
    cat << 'EOF' > /home/user/app/server.py
import sys
import time

if len(sys.argv) < 2:
    sys.exit(0)

input_str = sys.argv[1]
if "ZXQPLM" in input_str:
    time.sleep(0.6)
    print("Processed slowly")
else:
    print("Processed fast")
EOF
    chmod +x /home/user/app/server.py

    chmod -R 777 /home/user