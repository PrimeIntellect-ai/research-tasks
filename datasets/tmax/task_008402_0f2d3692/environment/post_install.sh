apt-get update && apt-get install -y python3 python3-pip g++ libsqlite3-dev sqlite3
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    sqlite3 /home/user/backup_metadata.db <<EOF
CREATE TABLE datacenters (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO datacenters VALUES (1, 'DC-Alpha'), (2, 'DC-Beta'), (3, 'DC-Gamma'), (4, 'DC-Omega');

CREATE TABLE replication_links (source_id INTEGER, target_id INTEGER, latency_ms INTEGER);
INSERT INTO replication_links VALUES (1, 2, 10), (2, 4, 20), (1, 3, 5), (3, 4, 10);

CREATE TABLE backup_jobs (id INTEGER PRIMARY KEY, dc_id INTEGER, status TEXT);
INSERT INTO backup_jobs VALUES (101, 1, 'SUCCESS'), (102, 2, 'SUCCESS'), (103, 3, 'FAILED'), (104, 4, 'SUCCESS');
EOF

    cat << 'EOF' > /home/user/backup_analyzer.cpp
#include <iostream>
#include <vector>
#include <string>
#include <sqlite3.h>
#include <fstream>
#include <queue>
#include <limits>

using namespace std;

struct Edge {
    int target;
    int latency;
};

// TODO: Fix the SQL query to avoid the implicit cross join and filter by target status = 'SUCCESS'
const char* SQL_QUERY = "SELECT r.source_id, r.target_id, r.latency_ms FROM replication_links r, backup_jobs b WHERE b.status = 'SUCCESS'";

void findShortestPath(int start_node, int end_node, sqlite3* db) {
    sqlite3_stmt* stmt;
    if (sqlite3_prepare_v2(db, SQL_QUERY, -1, &stmt, nullptr) != SQLITE_OK) {
        cerr << "Failed to prepare query" << endl;
        return;
    }

    // Build the graph: adjacency list where graph[source] = vector<Edge>
    // IMPLEMENTATION REQUIRED

    // Implement Dijkstra's algorithm to find shortest path from start_node to end_node
    // IMPLEMENTATION REQUIRED

    // Write output to /home/user/optimal_backup_path.json
    // IMPLEMENTATION REQUIRED

    sqlite3_finalize(stmt);
}

int main() {
    sqlite3* db;
    if (sqlite3_open("/home/user/backup_metadata.db", &db) != SQLITE_OK) {
        cerr << "Failed to open DB" << endl;
        return 1;
    }

    findShortestPath(1, 4, db);

    sqlite3_close(db);
    return 0;
}
EOF

    chown -R user:user /home/user/backup_metadata.db /home/user/backup_analyzer.cpp
    chmod -R 777 /home/user