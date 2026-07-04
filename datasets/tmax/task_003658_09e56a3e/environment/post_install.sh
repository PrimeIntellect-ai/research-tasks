apt-get update && apt-get install -y python3 python3-pip sqlite3 libsqlite3-dev gcc build-essential
    pip3 install pytest

    mkdir -p /app

    # Generate datasets.db
    cat << 'EOF' > /app/generate_db.py
import sqlite3
import random
import datetime

conn = sqlite3.connect('/app/datasets.db')
c = conn.cursor()
c.execute('CREATE TABLE datasets (id TEXT, name TEXT, size INTEGER, created_at TEXT)')
c.execute('CREATE TABLE dependencies (source_id TEXT, target_id TEXT)')

datasets = []
for i in range(1, 10001):
    id_str = f"ds_{i:05d}"
    if i == 1:
        id_str = "root_001"
    size = random.randint(500, 5000)
    created_at = datetime.datetime.now().isoformat()
    datasets.append((id_str, f"Dataset {i}", size, created_at))

c.executemany('INSERT INTO datasets VALUES (?, ?, ?, ?)', datasets)

edges = set()
for i in range(2, 200):
    edges.add(("root_001", f"ds_{i:05d}"))

for _ in range(25000 - len(edges)):
    u = random.randint(2, 9999)
    v = random.randint(u + 1, 10000)
    edges.add((f"ds_{u:05d}", f"ds_{v:05d}"))

c.executemany('INSERT INTO dependencies VALUES (?, ?)', list(edges))
conn.commit()
conn.close()
EOF
    python3 /app/generate_db.py

    # Create oracle Python script
    cat << 'EOF' > /app/oracle.py
import sys
import sqlite3
import json

if len(sys.argv) < 3:
    sys.exit(1)

root = sys.argv[1]
page = int(sys.argv[2])

conn = sqlite3.connect('/app/datasets.db')
c = conn.cursor()

visited = set()
stack = [root]
while stack:
    curr = stack.pop()
    c.execute('SELECT target_id FROM dependencies WHERE source_id = ?', (curr,))
    for row in c.fetchall():
        if row[0] not in visited:
            visited.add(row[0])
            stack.append(row[0])

if root in visited:
    visited.remove(root)

res = []
for node in visited:
    c.execute('SELECT id, size, created_at FROM datasets WHERE id = ?', (node,))
    row = c.fetchone()
    if row and row[1] >= 1024:
        res.append(row)

res.sort(key=lambda x: (-x[1], x[2], x[0]))
start = (page - 1) * 50
end = page * 50
page_res = [x[0] for x in res[start:end]]

print(json.dumps(page_res))
EOF

    # Create C wrapper for oracle
    cat << 'EOF' > /app/dataset_oracle.c
#include <stdlib.h>
#include <stdio.h>
int main(int argc, char *argv[]) {
    if (argc < 3) return 1;
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "python3 /app/oracle.py %s %s", argv[1], argv[2]);
    int ret = system(cmd);
    return ret;
}
EOF

    gcc -O3 /app/dataset_oracle.c -o /app/dataset_oracle
    strip /app/dataset_oracle
    chmod +x /app/dataset_oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user