apt-get update && apt-get install -y python3 python3-pip sqlite3
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import sqlite3
import os

db_path = '/home/user/financial_audit.db'
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute('CREATE TABLE entities (id INTEGER PRIMARY KEY, name TEXT)')
cursor.execute('CREATE TABLE transfers (tx_id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER, amount REAL)')

# Insert entities
entities = [
    (1, 'Nexus_Global'),
    (2, 'Alpha_Group'),
    (3, 'Beta_Holdings'),
    (4, 'Gamma_Corp'),
    (5, 'Delta_Inc'),
    (6, 'Apex_Solutions')
]
cursor.executemany('INSERT INTO entities VALUES (?, ?)', entities)

# Insert standard transfers
transfers = [
    (101, 1, 2, 50000),
    (102, 2, 3, 49000),
    (103, 3, 6, 48000),
    (104, 1, 4, 10000),
    (105, 4, 6, 9000)
]
cursor.executemany('INSERT INTO transfers VALUES (?, ?, ?, ?)', transfers)

# Create index
cursor.execute('CREATE INDEX idx_sender ON transfers(sender_id)')

# Insert the "hidden" transfers
cursor.execute('INSERT INTO transfers VALUES (106, 1, 5, 250000)')
cursor.execute('INSERT INTO transfers VALUES (107, 5, 6, 245000)')

conn.commit()
conn.close()
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user