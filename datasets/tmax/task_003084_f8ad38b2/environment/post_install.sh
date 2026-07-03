apt-get update && apt-get install -y python3 python3-pip gcc binutils
    pip3 install pytest

    mkdir -p /home/user/dataset
    mkdir -p /app

    # Generate the SQLite database
    cat << 'EOF' > /tmp/generate_db.py
import sqlite3
import random

random.seed(42)
conn = sqlite3.connect('/home/user/dataset/collaborations.db')
c = conn.cursor()
c.execute('CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT)')
c.execute('CREATE TABLE coauthors (author1 INTEGER, author2 INTEGER)')
c.execute('CREATE INDEX idx_coauthors ON coauthors(author1)')

# Generate a connected graph of 2000 nodes, 10000 edges
for i in range(1, 2001):
    c.execute('INSERT INTO authors (id, name) VALUES (?, ?)', (i, f'Author_{i}'))

edges = set()
for i in range(2, 2001):
    # Connect to a random previous node to ensure connectivity
    edges.add((random.randint(1, i-1), i))
    edges.add((i, random.randint(1, i-1)))

for _ in range(8000):
    u = random.randint(1, 2000)
    v = random.randint(1, 2000)
    if u != v:
        edges.add((u, v))
        edges.add((v, u))

c.executemany('INSERT INTO coauthors (author1, author2) VALUES (?, ?)', list(edges))
conn.commit()
conn.close()
EOF
    python3 /tmp/generate_db.py

    # Create the buggy script
    cat << 'EOF' > /home/user/generate_report.py
import sqlite3
import json
import sys

def main():
    conn = sqlite3.connect('/home/user/dataset/collaborations.db')
    cursor = conn.cursor()

    # BUG: The recursive step is missing 'WHERE author_paths.id = coauthors.author1'
    # This causes a massive cross join.
    query = """
    WITH RECURSIVE author_paths(id, distance) AS (
        SELECT 1, 0
        UNION ALL
        SELECT coauthors.author2, author_paths.distance + 1
        FROM author_paths, coauthors
        LIMIT 100000 -- Put here to stop the cross join from crashing the OS
    )
    SELECT id, MIN(distance) FROM author_paths GROUP BY id;
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        output = {str(row[0]): row[1] for row in results}
        with open('/home/user/distances.json', 'w') as f:
            json.dump(output, f)

    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()
EOF

    # Create a dummy oracle binary
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
int main() {
    return 0;
}
EOF
    gcc -O2 /tmp/oracle.c -o /app/path_oracle
    strip /app/path_oracle

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app