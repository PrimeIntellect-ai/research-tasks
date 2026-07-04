apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create dummy legacy calc
    mkdir -p /app
    cat << 'EOF' > /app/legacy_calc
#!/usr/bin/env python3
print("Legacy calc")
EOF
    chmod +x /app/legacy_calc

    # Generate data and expected output
    cat << 'EOF' > /tmp/generate_data.py
import sqlite3
import random
import json

db_path = "/home/user/backup_graph.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("CREATE TABLE backups (id TEXT PRIMARY KEY, parent_id TEXT, size_bytes INTEGER);")

nodes = []
roots = [f"root_{i}" for i in range(10)]
for r in roots:
    nodes.append((r, None, 100))

# Generate a deep/wide tree of 50,000 nodes
for i in range(50000):
    parent = random.choice(roots) if i < 100 else f"node_{random.randint(0, i-1)}"
    nodes.append((f"node_{i}", parent, random.randint(10, 100)))

c.executemany("INSERT INTO backups VALUES (?, ?, ?)", nodes)
conn.commit()

c.execute("""
WITH RECURSIVE cte AS (
    SELECT id AS root_id, id AS curr_id, size_bytes
    FROM backups WHERE parent_id IS NULL
    UNION ALL
    SELECT cte.root_id, b.id, b.size_bytes
    FROM cte JOIN backups b ON b.parent_id = cte.curr_id
)
SELECT root_id, SUM(size_bytes) FROM cte GROUP BY root_id;
""")
expected = {row[0]: row[1] for row in c.fetchall()}

with open("/tmp/expected_roots.json", "w") as f:
    json.dump(expected, f)

conn.close()
EOF

    python3 /tmp/generate_data.py

    chmod -R 777 /home/user