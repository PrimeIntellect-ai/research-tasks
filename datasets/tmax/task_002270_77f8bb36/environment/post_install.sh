apt-get update && apt-get install -y python3 python3-pip sqlite3 redis-server socat netcat-openbsd
    pip3 install pytest

    mkdir -p /app/data /app/service /app/etl

    # Populate SQLite DB
    cat << 'EOF' > /tmp/init_db.py
import sqlite3
import random

conn = sqlite3.connect('/app/data/graph.db')
c = conn.cursor()
c.execute('CREATE TABLE nodes(id INTEGER PRIMARY KEY)')
c.execute('CREATE TABLE edges(source INTEGER, target INTEGER)')

nodes = list(range(1, 1001))
c.executemany('INSERT INTO nodes(id) VALUES (?)', [(n,) for n in nodes])

edges = []
for _ in range(5000):
    edges.append((random.choice(nodes), random.choice(nodes)))

c.executemany('INSERT INTO edges(source, target) VALUES (?, ?)', edges)
c.execute('CREATE INDEX bad_idx ON edges(source)')

conn.commit()
conn.close()
EOF
    python3 /tmp/init_db.py
    rm /tmp/init_db.py

    # Skeleton query_server.sh
    cat << 'EOF' > /app/service/query_server.sh
#!/bin/bash
# Listen on port 8080 and respond to queries
EOF
    chmod +x /app/service/query_server.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app