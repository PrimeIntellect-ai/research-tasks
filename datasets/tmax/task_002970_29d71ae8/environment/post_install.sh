apt-get update && apt-get install -y python3 python3-pip redis-server sqlite3 curl
    pip3 install pytest redis flask requests

    mkdir -p /app/data /app/services /app/oracle

    # Create Flask API
    cat << 'EOF' > /app/services/flask_api.py
from flask import Flask, request, jsonify

app = Flask(__name__)

valid_edges = {
    ("node_1", "node_2"): True,
    ("node_2", "node_3"): True,
    ("node_1", "node_4"): False,
    ("node_4", "node_5"): True,
}

@app.route('/api/validate', methods=['GET'])
def validate():
    source = request.args.get('source')
    target = request.args.get('target')
    is_valid = valid_edges.get((source, target), False)
    return jsonify({"valid": is_valid})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

    # Create SQLite Database
    cat << 'EOF' > /tmp/setup_db.py
import sqlite3
conn = sqlite3.connect('/app/data/graph_backup.db')
c = conn.cursor()
c.execute('CREATE TABLE edges(source TEXT, target TEXT, weight REAL)')
edges = [
    ('node_1', 'node_2', 1.0),
    ('node_2', 'node_3', 1.0),
    ('node_1', 'node_4', 1.0),
    ('node_4', 'node_5', 1.0),
]
c.executemany("INSERT INTO edges VALUES (?, ?, ?)", edges)
conn.commit()
conn.close()
EOF
    python3 /tmp/setup_db.py

    # Populate Redis
    cd /
    redis-server --port 6379 --daemonize yes
    sleep 2
    redis-cli set node:node_1:status active
    redis-cli set node:node_2:status active
    redis-cli set node:node_3:status active
    redis-cli set node:node_4:status active
    redis-cli set node:node_5:status deleted
    redis-cli save
    redis-cli shutdown
    # Copy dump.rdb to common working directories just in case
    cp /dump.rdb /app/ || true
    cp /dump.rdb /root/ || true

    # Create Oracle
    cat << 'EOF' > /app/oracle/graph_query_oracle.py
#!/usr/bin/env python3
import sys
import sqlite3
import redis
import requests
import json

def get_valid_edges():
    conn = sqlite3.connect('/app/data/graph_backup.db')
    c = conn.cursor()
    c.execute('SELECT source, target FROM edges')
    edges = c.fetchall()
    conn.close()

    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

    valid = []
    for src, tgt in edges:
        if r.get(f"node:{src}:status") == "active" and r.get(f"node:{tgt}:status") == "active":
            try:
                resp = requests.get(f"http://127.0.0.1:8080/api/validate?source={src}&target={tgt}").json()
                if resp.get("valid"):
                    valid.append((src, tgt))
            except:
                pass
    return valid

def main():
    if len(sys.argv) < 2:
        return
    start_node = sys.argv[1]
    edges = get_valid_edges()

    graph = {}
    for src, tgt in edges:
        graph.setdefault(src, []).append(tgt)

    hop1 = set(graph.get(start_node, []))
    hop2 = set()
    for n in hop1:
        hop2.update(graph.get(n, []))

    hop2 -= hop1
    hop2.discard(start_node)

    print(json.dumps({"node": start_node, "1_hop": len(hop1), "2_hop": len(hop2)}))

if __name__ == "__main__":
    main()
EOF
    chmod +x /app/oracle/graph_query_oracle.py

    useradd -m -s /bin/bash user || true
    cp /dump.rdb /home/user/ || true
    chmod -R 777 /home/user
    chmod -R 777 /app