apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        sqlite3 \
        libsqlite3-dev \
        g++ \
        nlohmann-json3-dev \
        binutils

    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user/deps

    # Generate DB and JSON files
    cat << 'EOF' > /tmp/gen_data.py
import sqlite3
import json
import random
import os

os.makedirs('/home/user/deps', exist_ok=True)
conn = sqlite3.connect('/home/user/db_inventory.db')
c = conn.cursor()
c.execute('CREATE TABLE restore_points (id INTEGER, snapshot_name TEXT, environment TEXT)')
c.execute('CREATE TABLE datacenter_map (environment TEXT, datacenter_name TEXT, cost_multiplier REAL)')

envs = ['prod', 'staging', 'dev', 'qa', 'dr']
for env in envs:
    c.execute('INSERT INTO datacenter_map VALUES (?, ?, ?)', (env, f'dc_{env}', random.uniform(1.0, 5.0)))

for i in range(1, 501):
    env = random.choice(envs)
    c.execute('INSERT INTO restore_points VALUES (?, ?, ?)', (i, f'snap_{i}', env))

    edges = []
    num_edges = random.randint(2, 10)
    for _ in range(num_edges):
        target = random.randint(1, 500)
        if target != i:
            edges.append({"target_id": target, "base_cost": random.randint(1, 100)})

    with open(f'/home/user/deps/{i}.json', 'w') as f:
        json.dump(edges, f)

conn.commit()
conn.close()
EOF
    python3 /tmp/gen_data.py

    # Create C++ oracle
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <queue>
#include <sqlite3.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 3) return 1;
    int src = stoi(argv[1]);
    int dst = stoi(argv[2]);

    sqlite3* db;
    if (sqlite3_open("/home/user/db_inventory.db", &db)) return 1;

    map<int, double> multipliers;
    const char* query = "SELECT r.id, d.cost_multiplier FROM restore_points r JOIN datacenter_map d ON r.environment = d.environment;";
    sqlite3_stmt* stmt;
    if (sqlite3_prepare_v2(db, query, -1, &stmt, 0) == SQLITE_OK) {
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            double mult = sqlite3_column_double(stmt, 1);
            multipliers[id] = mult;
        }
    }
    sqlite3_finalize(stmt);
    sqlite3_close(db);

    map<int, vector<pair<int, double>>> graph;
    for (int i = 1; i <= 500; ++i) {
        string path = "/home/user/deps/" + to_string(i) + ".json";
        ifstream f(path);
        if (!f.is_open()) continue;
        json j;
        f >> j;
        double mult = multipliers[i];
        for (auto& edge : j) {
            int target = edge["target_id"];
            double cost = edge["base_cost"];
            graph[i].push_back({target, cost * mult});
        }
    }

    priority_queue<pair<double, int>, vector<pair<double, int>>, greater<pair<double, int>>> pq;
    map<int, double> dist;
    map<int, int> parent;
    for (int i = 1; i <= 500; ++i) dist[i] = 1e18;

    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;
        if (u == dst) break;

        for (auto& edge : graph[u]) {
            int v = edge.first;
            double weight = edge.second;
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                parent[v] = u;
                pq.push({dist[v], v});
            }
        }
    }

    if (dist[dst] == 1e18) {
        cout << "UNREACHABLE" << endl;
    } else {
        vector<int> path;
        for (int v = dst; v != 0; v = parent[v]) {
            path.push_back(v);
            if (v == src) break;
        }
        for (int i = path.size() - 1; i >= 0; --i) {
            cout << path[i] << (i == 0 ? "" : ",");
        }
        cout << endl;
    }

    return 0;
}
EOF
    g++ -O3 -o /app/oracle_planner /tmp/oracle.cpp -lsqlite3
    strip /app/oracle_planner

    # Create buggy starter script
    cat << 'EOF' > /home/user/query_builder.py
import sqlite3

def get_multipliers():
    conn = sqlite3.connect('/home/user/db_inventory.db')
    c = conn.cursor()
    # BUG: Cross join missing WHERE r.environment = d.environment
    c.execute('SELECT r.id, d.cost_multiplier FROM restore_points r, datacenter_map d;')
    results = c.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    print(get_multipliers()[:10])
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user