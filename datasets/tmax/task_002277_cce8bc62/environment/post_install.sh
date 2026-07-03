apt-get update && apt-get install -y python3 python3-pip redis-server curl
    pip3 install pytest flask requests networkx redis

    mkdir -p /app
    cd /app

    # Generate graph.db
    cat << 'EOF' > generate_db.py
import sqlite3
import random

conn = sqlite3.connect('/app/graph.db')
c = conn.cursor()
c.execute("CREATE TABLE edges (source INTEGER, target INTEGER, weight REAL)")
edges = []
for _ in range(100000):
    edges.append((random.randint(1, 1000), random.randint(1, 1000), random.random()))
c.executemany("INSERT INTO edges VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
EOF
    python3 generate_db.py
    rm generate_db.py

    # Create sqlite_server.py
    cat << 'EOF' > /app/sqlite_server.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/edges')
def get_edges():
    min_w = request.args.get('min_weight', 0.0)
    conn = sqlite3.connect('/app/graph.db')
    c = conn.cursor()
    c.execute("SELECT source, target FROM edges WHERE weight >= ?", (min_w,))
    rows = c.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(port=5001)
EOF

    # Create etl_api.py
    cat << 'EOF' > /app/etl_api.py
from flask import Flask, jsonify
import requests
import networkx as nx
import redis
import json

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/pagerank')
def pagerank():
    cached = r.get('top_pagerank')
    if cached:
        return jsonify(json.loads(cached))

    # TODO: Fetch edges, compute PageRank, get top 10, cache in Redis, return
    return jsonify([])

if __name__ == '__main__':
    app.run(port=5000)
EOF

    # Create start.sh
    cat << 'EOF' > /app/start.sh
#!/bin/bash
redis-server --daemonize yes
python3 /app/sqlite_server.py &
python3 /app/etl_api.py &
wait
EOF
    chmod +x /app/start.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user