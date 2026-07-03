apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import random
import heapq

os.makedirs('/home/user/data', exist_ok=True)

# Generate a deterministic graph
random.seed(42)
num_nodes = 5000
num_edges = 40000
edges = set()

with open('/home/user/data/edges.csv', 'w') as f:
    for _ in range(num_edges):
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v:
            w = random.randint(10, 500)
            if (u, v) not in edges:
                edges.add((u, v))
                f.write(f"{u},{v},{w}\n")

# Generate queries
num_queries = 2000
queries = []
with open('/home/user/data/queries.csv', 'w') as f:
    for _ in range(num_queries):
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        queries.append((u, v))
        f.write(f"{u},{v}\n")

# Compute truth
adj = {i: [] for i in range(num_nodes)}
for u, v in edges:
    pass

with open('/home/user/data/edges.csv', 'r') as f:
    for line in f:
        u, v, w = map(int, line.strip().split(','))
        adj[u].append((v, w))

results = []
for u, target in queries:
    if u == target:
        results.append((u, target, 0))
        continue

    dist = {u: 0}
    pq = [(0, u)]
    found = False

    while pq:
        d, curr = heapq.heappop(pq)

        if d > dist.get(curr, float('inf')):
            continue

        if curr == target:
            results.append((u, target, d))
            found = True
            break

        for nxt, w in adj[curr]:
            new_d = d + w
            if new_d < dist.get(nxt, float('inf')):
                dist[nxt] = new_d
                heapq.heappush(pq, (new_d, nxt))

# Filter, Sort, Paginate
filtered = [r for r in results if r[2] <= 5000]
filtered.sort(key=lambda x: (x[2], x[0], x[1]))
paginated = filtered[10:30]

with open('/home/user/expected_result.csv', 'w') as f:
    for u, v, d in paginated:
        f.write(f"{u},{v},{d}\n")
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user