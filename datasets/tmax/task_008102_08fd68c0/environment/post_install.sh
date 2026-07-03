apt-get update && apt-get install -y python3 python3-pip sqlite3
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user

    cat << 'EOF' > /tmp/setup.py
import sqlite3
import random
import json
import os

os.makedirs('/home/user', exist_ok=True)
db_path = '/home/user/ecommerce_graph.db'
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, is_active INTEGER)')
c.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)')
c.execute('CREATE TABLE views (user_id INTEGER, product_id INTEGER, view_date TEXT)')
c.execute('CREATE TABLE purchases (user_id INTEGER, product_id INTEGER, purchase_date TEXT)')

random.seed(42)

categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Toys', 'Sports', 'Beauty']
for i in range(1, 1001):
    c.execute('INSERT INTO products (id, name, category, price) VALUES (?, ?, ?, ?)', 
              (i, f'Product_{i}', random.choice(categories), round(random.uniform(10, 100), 2)))

for i in range(1, 501):
    c.execute('INSERT INTO users (id, name, is_active) VALUES (?, ?, ?)', 
              (i, f'User_{i}', random.choice([0, 1])))

for _ in range(5000):
    u = random.randint(1, 500)
    p = random.randint(1, 1000)
    c.execute('INSERT INTO views (user_id, product_id, view_date) VALUES (?, ?, ?)', 
              (u, p, '2023-01-01'))

for _ in range(3000):
    u = random.randint(1, 500)
    p = random.randint(1, 1000)
    c.execute('INSERT INTO purchases (user_id, product_id, purchase_date) VALUES (?, ?, ?)', 
              (u, p, '2023-01-02'))

conn.commit()

# Compute the ground truth expected output
c.execute('''
    WITH TargetUsers AS (
        SELECT u.id
        FROM users u
        WHERE u.is_active = 1
          AND EXISTS (
              SELECT 1 FROM views v
              JOIN products p ON v.product_id = p.id
              WHERE v.user_id = u.id AND p.category = 'Electronics'
          )
          AND NOT EXISTS (
              SELECT 1 FROM purchases pu
              JOIN products p ON pu.product_id = p.id
              WHERE pu.user_id = u.id AND p.category = 'Electronics'
          )
    )
    SELECT p.category, COUNT(*) as purchase_count
    FROM purchases pu
    JOIN products p ON pu.product_id = p.id
    JOIN TargetUsers tu ON pu.user_id = tu.id
    GROUP BY p.category
    ORDER BY purchase_count DESC, p.category ASC
    LIMIT 5
''')

expected_result = [{"category": row[0], "purchase_count": row[1]} for row in c.fetchall()]

with open('/home/user/expected_solution.json', 'w') as f:
    json.dump(expected_result, f)

conn.close()
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user