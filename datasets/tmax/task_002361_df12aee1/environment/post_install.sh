apt-get update && apt-get install -y python3 python3-pip gcc liblapack-dev libblas-dev gawk bc curl
    pip3 install pytest

    mkdir -p /app/sim /app/logger /app/gateway

    # Create dummy files for services
    cat << 'EOF' > /app/sim/sim.c
#include <stdio.h>
int main() {
    printf("Simulation Daemon\n");
    return 0;
}
EOF

    cat << 'EOF' > /app/logger/logger.py
import sys
print("Telemetry Logger")
EOF

    cat << 'EOF' > /app/gateway/gateway.sh
#!/bin/bash
echo "API Gateway"
EOF
    chmod +x /app/gateway/gateway.sh

    # Create the oracle analyzer
    cat << 'EOF' > /app/oracle_analyzer
#!/usr/bin/env python3
import sys
from collections import defaultdict

def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        lines = [line.strip().split() for line in f if line.strip()]

    edges = defaultdict(list)
    in_degree = defaultdict(int)
    nodes = set()
    latencies = []

    for u, v, w in lines:
        w = int(w)
        edges[u].append((v, w))
        in_degree[v] += 1
        nodes.add(u)
        nodes.add(v)
        latencies.append(w)

    if not latencies:
        return

    for n in nodes:
        if n not in in_degree:
            in_degree[n] = 0

    q = sorted([n for n in nodes if in_degree[n] == 0])
    topo = []
    while q:
        u = q.pop(0)
        topo.append(u)
        for v, w in edges[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                q.append(v)
        q.sort()

    dist = {n: 0 for n in nodes}
    path = {n: [n] for n in nodes}

    for u in topo:
        for v, w in edges[u]:
            if dist[u] + w > dist[v]:
                dist[v] = dist[u] + w
                path[v] = path[u] + [v]
            elif dist[u] + w == dist[v]:
                p1 = "->".join(path[u] + [v])
                p2 = "->".join(path[v])
                if p1 < p2:
                    path[v] = path[u] + [v]

    max_dist = -1
    best_path = []
    for n in nodes:
        if dist[n] > max_dist:
            max_dist = dist[n]
            best_path = path[n]
        elif dist[n] == max_dist:
            p1 = "->".join(path[n])
            p2 = "->".join(best_path)
            if p1 < p2:
                best_path = path[n]

    print(f"Path: {'->'.join(best_path)}, Total: {max_dist}")

    MIN = min(latencies)
    MAX = max(latencies)
    W = (MAX - MIN) / 5.0

    b1=b2=b3=b4=b5=0
    for w in latencies:
        if w < MIN + W: b1+=1
        elif w < MIN + 2*W: b2+=1
        elif w < MIN + 3*W: b3+=1
        elif w < MIN + 4*W: b4+=1
        else: b5+=1

    print(f"Density: B1:{b1}, B2:{b2}, B3:{b3}, B4:{b4}, B5:{b5}")

if __name__ == '__main__':
    main()
EOF
    chmod +x /app/oracle_analyzer

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user