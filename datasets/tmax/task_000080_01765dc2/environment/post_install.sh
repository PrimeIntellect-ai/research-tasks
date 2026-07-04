apt-get update && apt-get install -y python3 python3-pip sqlite3 espeak
    pip3 install pytest

    mkdir -p /home/user/data
    mkdir -p /app

    # Create the audio file
    espeak -w /app/requirements.wav "We need to calculate the total transaction volume for each region, but only for active accounts. Join the accounts, transactions, and regions tables. Sum the transaction amounts where the account status is active. Output the final aggregated list to slash home slash user slash report dot csv ordered by volume descending."

    # Setup database
    cat << 'EOF' > /tmp/setup_db.py
import sqlite3
import os

os.makedirs('/home/user/data', exist_ok=True)
conn = sqlite3.connect('/home/user/data/warehouse.db')
c = conn.cursor()

c.execute("CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT)")
c.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, region_id INTEGER, status TEXT)")
c.execute("CREATE TABLE transactions (id INTEGER PRIMARY KEY, account_id INTEGER, amount REAL)")

c.execute("INSERT INTO regions (id, name) VALUES (1, 'North America'), (2, 'Europe'), (3, 'Asia')")
c.execute("INSERT INTO accounts (id, region_id, status) VALUES (1, 1, 'active'), (2, 2, 'active'), (3, 3, 'active')")
c.execute("INSERT INTO transactions (id, account_id, amount) VALUES (1, 1, 150400.50), (2, 2, 120300.25), (3, 3, 98000.00)")

inactive_accounts = [(i, (i%3)+1, 'inactive') for i in range(4, 1000)]
c.executemany("INSERT INTO accounts (id, region_id, status) VALUES (?, ?, ?)", inactive_accounts)

transactions = [(i, (i%996)+4, 10.0) for i in range(4, 500000)]
c.executemany("INSERT INTO transactions (id, account_id, amount) VALUES (?, ?, ?)", transactions)

conn.commit()
conn.close()
EOF
    python3 /tmp/setup_db.py

    # Create the unoptimized bash script
    cat << 'EOF' > /home/user/process.sh
#!/bin/bash

# Simulate concurrent queries and slow execution
sleep 20

sqlite3 /home/user/data/warehouse.db << 'SQL'
.mode csv
.headers off
SELECT r.name, printf("%.2f", SUM(t.amount))
FROM regions r
JOIN accounts a ON r.id = a.region_id
JOIN transactions t ON a.id = t.account_id
WHERE a.status = 'active'
GROUP BY r.name
ORDER BY SUM(t.amount) DESC;
SQL
EOF

    # Output to file
    sed -i 's/ORDER BY SUM(t.amount) DESC;/ORDER BY SUM(t.amount) DESC;\n.output \/home\/user\/report.csv/' /home/user/process.sh
    # Actually just rewrite the script properly
    cat << 'EOF' > /home/user/process.sh
#!/bin/bash
sleep 20
sqlite3 /home/user/data/warehouse.db -csv "SELECT r.name, printf('%.2f', SUM(t.amount)) FROM regions r JOIN accounts a ON r.id = a.region_id JOIN transactions t ON a.id = t.account_id WHERE a.status = 'active' GROUP BY r.name ORDER BY SUM(t.amount) DESC;" > /home/user/report.csv
EOF

    chmod +x /home/user/process.sh

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user