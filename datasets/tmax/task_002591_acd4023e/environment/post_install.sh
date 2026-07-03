apt-get update && apt-get install -y python3 python3-pip espeak sqlite3 ffmpeg
    pip3 install pytest

    mkdir -p /app

    # Generate Audio
    espeak -w /app/instructions.wav "Please ensure that any dataset with the tag deprecated is completely ignored by the traversal. Also, the frontend requires the pagination page size to be exactly fourteen."

    # Generate DB
    cat << 'EOF' > /tmp/gen_db.py
import sqlite3
import random

random.seed(42)
conn = sqlite3.connect('/app/research_data.db')
c = conn.cursor()
c.execute('CREATE TABLE datasets (id INTEGER PRIMARY KEY, name TEXT, tag TEXT)')
c.execute('CREATE TABLE lineage (source_id INTEGER, target_id INTEGER)')

tags = ['active', 'archived', 'deprecated', 'review']
for i in range(1, 201):
    c.execute('INSERT INTO datasets (id, name, tag) VALUES (?, ?, ?)', (i, f'dataset_{i}', random.choice(tags)))

edges = set()
while len(edges) < 400:
    src = random.randint(1, 199)
    tgt = random.randint(src + 1, 200)
    edges.add((src, tgt))

for src, tgt in edges:
    c.execute('INSERT INTO lineage (source_id, target_id) VALUES (?, ?)', (src, tgt))

conn.commit()
conn.close()
EOF
    python3 /tmp/gen_db.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user