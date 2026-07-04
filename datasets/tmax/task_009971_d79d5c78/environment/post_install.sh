apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import random
from collections import defaultdict

os.makedirs('/home/user/data', exist_ok=True)

random.seed(42)
num_nodes = 5000
num_edges = 50000
num_queries = 200

edges = set()
while len(edges) < num_edges:
    u = random.randint(1, num_nodes)
    v = random.randint(1, num_nodes)
    if u != v:
        w = round(random.uniform(0.1, 10.0), 2)
        edges.add((u, v, w))

edges_list = list(edges)
adj = defaultdict(list)
with open('/home/user/data/edges.csv', 'w') as f:
    for u, v, w in edges_list:
        f.write(f"{u},{v},{w:.2f}\n")
        adj[u].append((v, w))

queries = []
for _ in range(num_queries):
    start_node = random.randint(1, num_nodes)
    min_w = round(random.uniform(5.0, 15.0), 2)
    queries.append((start_node, min_w))

with open('/home/user/data/queries.csv', 'w') as f:
    for u, w in queries:
        f.write(f"{u},{w:.2f}\n")

# Compute ground truth
with open('/home/user/expected_results.csv', 'w') as f:
    for start_node, min_w in queries:
        valid_c = set()
        for b, w1 in adj.get(start_node, []):
            for c, w2 in adj.get(b, []):
                if start_node != b and b != c and start_node != c:
                    if w1 + w2 >= min_w:
                        valid_c.add(c)
        f.write(f"{start_node},{min_w:.2f},{len(valid_c)}\n")
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user