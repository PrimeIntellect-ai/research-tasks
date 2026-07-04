apt-get update && apt-get install -y python3 python3-pip build-essential libsqlite3-dev sqlite3
    pip3 install --default-timeout=100 pytest

    mkdir -p /app/libfastgraph-1.2.0/include
    mkdir -p /app/libfastgraph-1.2.0/src
    mkdir -p /home/user

    cat << 'EOF' > /app/libfastgraph-1.2.0/Makefile
CXX = g++
CXXFLAGS = -O0 -I./include -std=c++11

all: lib/libfastgraph.a

lib/libfastgraph.a: src/fastgraph.o
	mkdir -p lib
	ar rcs $@ $^

src/fastgraph.o: src/fastgraph.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

install:
	mkdir -p $(PREFIX)/include $(PREFIX)/lib
	cp include/*.h $(PREFIX)/include/
	cp lib/*.a $(PREFIX)/lib/

clean:
	rm -rf src/*.o lib
EOF

    cat << 'EOF' > /app/libfastgraph-1.2.0/include/fastgraph_config.h
#ifndef FASTGRAPH_CONFIG_H
#define FASTGRAPH_CONFIG_H

#define DISABLE_CACHE 1

#endif
EOF

    cat << 'EOF' > /app/libfastgraph-1.2.0/include/fastgraph.h
#ifndef FASTGRAPH_H
#define FASTGRAPH_H

#include <vector>
#include <map>

class FastGraph {
public:
    void add_edge(int source, int target, double weight);
    std::map<int, double> compute_pagerank(int iterations = 20, double damping = 0.85);
private:
    struct Edge {
        int target;
        double weight;
    };
    std::map<int, std::vector<Edge>> adj;
    std::vector<int> nodes;
};

#endif
EOF

    cat << 'EOF' > /app/libfastgraph-1.2.0/src/fastgraph.cpp
#include "fastgraph.h"
#include "fastgraph_config.h"
#include <cmath>
#include <iostream>
#include <set>

void FastGraph::add_edge(int source, int target, double weight) {
    adj[source].push_back({target, weight});
    nodes.push_back(source);
    nodes.push_back(target);
}

std::map<int, double> FastGraph::compute_pagerank(int iterations, double damping) {
    std::set<int> unique_nodes(nodes.begin(), nodes.end());
    std::map<int, double> pr;
    int N = unique_nodes.size();
    if (N == 0) return pr;

    for (int node : unique_nodes) {
        pr[node] = 1.0 / N;
    }

    for (int iter = 0; iter < iterations; ++iter) {
        std::map<int, double> new_pr;
        for (int node : unique_nodes) {
            new_pr[node] = (1.0 - damping) / N;
        }

        for (auto const& pair : adj) {
            int u = pair.first;
            double sum_weights = 0;
            for (auto const& edge : pair.second) sum_weights += edge.weight;

            if (sum_weights > 0) {
                for (auto const& edge : pair.second) {
                    int v = edge.target;
                    new_pr[v] += damping * pr[u] * (edge.weight / sum_weights);
                }
            }
#if DISABLE_CACHE == 1
            double dummy = 0;
            for (int i = 0; i < 50000; ++i) {
                dummy += std::sin(i);
            }
            if (dummy > 1000000) pr[u] = dummy;
#endif
        }
        pr = new_pr;
    }
    return pr;
}
EOF

    cat << 'EOF' > /app/setup_data.py
import sqlite3
import random
import csv

random.seed(42)

conn = sqlite3.connect('/home/user/corporate.db')
c = conn.cursor()
c.execute('CREATE TABLE personnel (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, department TEXT)')
c.execute('CREATE TABLE interactions (source_id INTEGER, target_id INTEGER, interaction_weight REAL)')

# Generate 1000 employees
for i in range(1, 1001):
    manager = random.randint(1, i-1) if i > 1 else None
    c.execute('INSERT INTO personnel VALUES (?, ?, ?, ?)', (i, f'Emp_{i}', manager, 'Dept'))

# Generate interactions
for _ in range(5000):
    src = random.randint(1, 1000)
    tgt = random.randint(1, 1000)
    w = random.uniform(0.1, 2.0)
    c.execute('INSERT INTO interactions VALUES (?, ?, ?)', (src, tgt, w))

conn.commit()

# Compute golden pagerank
edges = {}
nodes = set(range(1, 1001))

c.execute('SELECT * FROM interactions')
for row in c.fetchall():
    src, tgt, w = row
    if src not in edges: edges[src] = {}
    edges[src][tgt] = edges[src].get(tgt, 0.0) + w

c.execute('SELECT id, manager_id FROM personnel')
managers = {row[0]: row[1] for row in c.fetchall()}

for emp in range(1, 1001):
    curr = emp
    weight = 1.0
    while managers.get(curr) is not None:
        mgr = managers[curr]
        if emp not in edges: edges[emp] = {}
        edges[emp][mgr] = edges[emp].get(mgr, 0.0) + weight
        curr = mgr
        weight *= 0.5

N = len(nodes)
pr = {n: 1.0/N for n in nodes}
for _ in range(20):
    new_pr = {n: (1.0 - 0.85)/N for n in nodes}
    for u in nodes:
        if u in edges:
            sum_w = sum(edges[u].values())
            if sum_w > 0:
                for v, w in edges[u].items():
                    new_pr[v] += 0.85 * pr[u] * (w / sum_w)
    pr = new_pr

with open('/app/golden_pagerank.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'pagerank'])
    for k, v in sorted(pr.items()):
        writer.writerow([k, v])

conn.close()
EOF

    python3 /app/setup_data.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user /app
    chmod -R 777 /home/user /app