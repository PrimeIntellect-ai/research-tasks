apt-get update && apt-get install -y python3 python3-pip rustc cargo libsqlite3-dev pkg-config
    pip3 install pytest pandas

    mkdir -p /app
    mkdir -p /home/user/auditor/src

    # Create schema image
    touch /app/schema.png

    # Generate database and truth data
    cat << 'EOF' > /tmp/setup_db.py
import sqlite3
import csv
import random

conn = sqlite3.connect('/home/user/financials.db')
c = conn.cursor()
c.execute('CREATE TABLE bank_accounts (acct_id INTEGER PRIMARY KEY, owner_name TEXT)')
c.execute('CREATE TABLE wire_transfers (tx_id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER, usd_amount REAL)')

accounts = [(i, f'Owner {i}') for i in range(1, 101)]
c.executemany('INSERT INTO bank_accounts VALUES (?, ?)', accounts)

transfers = []
tx_id = 1
for _ in range(200):
    s = random.randint(1, 100)
    r = random.randint(1, 100)
    if s != r:
        transfers.append((tx_id, s, r, 100.0))
        tx_id += 1

transfers.extend([
    (tx_id, 1, 2, 50.0),
    (tx_id+1, 2, 3, 50.0),
    (tx_id+2, 3, 1, 50.0),
    (tx_id+3, 10, 20, 50.0),
    (tx_id+4, 20, 30, 50.0),
    (tx_id+5, 30, 10, 50.0)
])
c.executemany('INSERT INTO wire_transfers VALUES (?, ?, ?, ?)', transfers)
conn.commit()

c.execute('''
    SELECT t1.sender_id, t2.sender_id, t3.sender_id 
    FROM wire_transfers t1
    JOIN wire_transfers t2 ON t1.receiver_id = t2.sender_id
    JOIN wire_transfers t3 ON t2.receiver_id = t3.sender_id
    WHERE t3.receiver_id = t1.sender_id
    ORDER BY t1.sender_id ASC
    LIMIT 1000
''')
truth = c.fetchall()

with open('/app/truth_cycles.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(truth)

conn.close()
EOF
    python3 /tmp/setup_db.py

    # Setup Rust project
    cat << 'EOF' > /home/user/auditor/Cargo.toml
[package]
name = "auditor"
version = "0.1.0"
edition = "2021"

[dependencies]
rusqlite = "0.29.0"
csv = "1.1"
EOF

    cat << 'EOF' > /home/user/auditor/src/main.rs
use rusqlite::{Connection, Result};
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let conn = Connection::open("/home/user/financials.db")?;
    let mut stmt = conn.prepare("
        SELECT t1.sender_id, t2.sender_id, t3.sender_id 
        FROM wire_transfers t1, wire_transfers t2, wire_transfers t3
        WHERE t1.receiver_id = t2.sender_id
          AND t3.receiver_id = t1.sender_id
        ORDER BY t1.sender_id ASC
        LIMIT 1000
    ")?;

    let cycle_iter = stmt.query_map([], |row| {
        Ok((row.get::<_, i32>(0)?, row.get::<_, i32>(1)?, row.get::<_, i32>(2)?))
    })?;

    let mut wtr = csv::Writer::from_path("/home/user/cycles.csv")?;
    for cycle in cycle_iter {
        let (a, b, c) = cycle?;
        wtr.write_record(&[a.to_string(), b.to_string(), c.to_string()])?;
    }
    wtr.flush()?;

    Ok(())
}
EOF

    # Pre-build dependencies to save time
    cd /home/user/auditor && cargo build || true

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app