apt-get update && apt-get install -y python3 python3-pip gcc binutils
    pip3 install --default-timeout=100 pytest networkx pandas

    mkdir -p /home/user/data
    mkdir -p /app

    # Create the C binary for path_oracle
    cat << 'EOF' > /app/path_oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NODES 10000
#define INF 1000000000

int adj[MAX_NODES][MAX_NODES];

void dijkstra(int src, int dst) {
    int dist[MAX_NODES];
    int visited[MAX_NODES];
    for (int i = 0; i < MAX_NODES; i++) {
        dist[i] = INF;
        visited[i] = 0;
    }
    dist[src] = 0;

    for (int count = 0; count < MAX_NODES - 1; count++) {
        int u = -1;
        for (int i = 0; i < MAX_NODES; i++) {
            if (!visited[i] && (u == -1 || dist[i] < dist[u])) {
                u = i;
            }
        }
        if (dist[u] == INF) break;
        visited[u] = 1;

        for (int v = 0; v < MAX_NODES; v++) {
            if (!visited[v] && adj[u][v] != INF && dist[u] != INF && dist[u] + adj[u][v] < dist[v]) {
                dist[v] = dist[u] + adj[u][v];
            }
        }
    }
    if (dist[dst] == INF) {
        printf("-1\n");
    } else {
        printf("%d\n", dist[dst]);
    }
    fflush(stdout);
}

int main() {
    for (int i = 0; i < MAX_NODES; i++) {
        for (int j = 0; j < MAX_NODES; j++) {
            adj[i][j] = INF;
        }
    }

    char line[256];
    while (fgets(line, sizeof(line), stdin)) {
        if (strncmp(line, "EDGE", 4) == 0) {
            int u, v, w;
            if (sscanf(line, "EDGE %d %d %d", &u, &v, &w) == 3) {
                if (u >= 0 && u < MAX_NODES && v >= 0 && v < MAX_NODES) {
                    adj[u][v] = w;
                }
            }
        } else if (strncmp(line, "ROUTE", 5) == 0) {
            int u, v;
            if (sscanf(line, "ROUTE %d %d", &u, &v) == 2) {
                if (u >= 0 && u < MAX_NODES && v >= 0 && v < MAX_NODES) {
                    dijkstra(u, v);
                } else {
                    printf("-1\n");
                    fflush(stdout);
                }
            }
        } else if (strncmp(line, "QUIT", 4) == 0) {
            break;
        }
    }
    return 0;
}
EOF

    gcc -O3 /app/path_oracle.c -o /app/path_oracle
    strip /app/path_oracle
    rm /app/path_oracle.c

    # Generate the data, sqlite db, and golden results
    cat << 'EOF' > /tmp/setup_data.py
import sqlite3
import random
import csv
import networkx as nx

random.seed(42)

conn = sqlite3.connect('/home/user/data/network.db')
c = conn.cursor()
c.execute('CREATE TABLE nodes(id INTEGER PRIMARY KEY, name TEXT)')
c.execute('CREATE TABLE edges(source INTEGER, target INTEGER, weight INTEGER)')

for i in range(200):
    c.execute('INSERT INTO nodes VALUES (?, ?)', (i, f'node_{i}'))

edges = {}
for _ in range(1000):
    u = random.randint(0, 199)
    v = random.randint(0, 199)
    w = random.randint(1, 100)
    if u != v:
        edges[(u, v)] = w
        c.execute('INSERT INTO edges VALUES (?, ?, ?)', (u, v, w))

c.execute('CREATE INDEX idx_edges_src ON edges(source)')
conn.commit()

# Corrupt the index to simulate stale reads
c.execute('CREATE TABLE fake_edges(source INTEGER, target INTEGER, weight INTEGER)')
for _ in range(100):
    c.execute('INSERT INTO fake_edges VALUES (?, ?, ?)', (random.randint(0, 199), random.randint(0, 199), 9999))
c.execute('CREATE INDEX fake_idx ON fake_edges(source)')
conn.commit()

c.execute('PRAGMA writable_schema = ON')
c.execute("UPDATE sqlite_master SET rootpage = (SELECT rootpage FROM sqlite_master WHERE name='fake_idx') WHERE name='idx_edges_src'")
conn.commit()
conn.close()

updates = []
for _ in range(100):
    u = random.randint(0, 199)
    v = random.randint(0, 199)
    w = random.randint(1, 100)
    if u != v:
        updates.append((u, v, w))
        edges[(u, v)] = w

with open('/home/user/data/updates.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(updates)

queries = []
for _ in range(100):
    u = random.randint(0, 199)
    v = random.randint(0, 199)
    queries.append((u, v))

with open('/home/user/data/queries.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(queries)

G = nx.DiGraph()
for (u, v), w in edges.items():
    G.add_edge(u, v, weight=w)

with open('/tmp/golden.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for u, v in queries:
        try:
            dist = nx.shortest_path_length(G, u, v, weight='weight')
        except nx.NetworkXNoPath:
            dist = -1
        writer.writerow([u, v, dist])
EOF

    python3 /tmp/setup_data.py
    rm /tmp/setup_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /tmp/golden.csv