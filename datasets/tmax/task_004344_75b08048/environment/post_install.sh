apt-get update && apt-get install -y python3 python3-pip gcc libsqlite3-dev sqlite3
    pip3 install pytest

    mkdir -p /app

    # Create the SQLite database
    sqlite3 /app/graph.db <<EOF
CREATE TABLE nodes (id INTEGER PRIMARY KEY, label TEXT);
CREATE TABLE edges (src INTEGER, dst INTEGER, weight REAL, FOREIGN KEY(src) REFERENCES nodes(id), FOREIGN KEY(dst) REFERENCES nodes(id));
CREATE INDEX idx_edges_src ON edges(src);
EOF

    # Create the C program for graph_oracle
    cat <<'EOF' > /app/graph_oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <query>\n", argv[0]);
        return 1;
    }
    sqlite3 *db;
    int rc = sqlite3_open("/app/graph.db", &db);
    if (rc) {
        fprintf(stderr, "Cannot open database\n");
        return 1;
    }

    char query[8192];
    snprintf(query, sizeof(query), "EXPLAIN QUERY PLAN %s", argv[1]);

    sqlite3_stmt *res;
    rc = sqlite3_prepare_v2(db, query, -1, &res, 0);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Error: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    while (sqlite3_step(res) == SQLITE_ROW) {
        const unsigned char *detail = sqlite3_column_text(res, 3);
        if (detail) {
            printf("%s\n", detail);
        }
    }

    sqlite3_finalize(res);
    sqlite3_close(db);
    return 0;
}
EOF

    # Compile and strip the binary
    gcc -o /app/graph_oracle /app/graph_oracle.c -lsqlite3
    strip /app/graph_oracle
    rm /app/graph_oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user