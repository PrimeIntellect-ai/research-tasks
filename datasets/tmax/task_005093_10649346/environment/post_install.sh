apt-get update && apt-get install -y python3 python3-pip sqlite3
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create the database and schema
    sqlite3 /home/user/data.db <<EOF
CREATE TABLE nodes (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE edges (source_id INTEGER, target_id INTEGER);
CREATE INDEX idx_edges_source ON edges(source_id);

WITH RECURSIVE cnt(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM cnt WHERE x<500)
INSERT INTO nodes(id, name) SELECT x, 'Node_' || x FROM cnt;
INSERT INTO edges(source_id, target_id) SELECT id, ((id * 7) % 500) + 1 FROM nodes;
INSERT INTO edges(source_id, target_id) SELECT id, ((id * 13) % 500) + 1 FROM nodes;
EOF

    # Create the oracle
    mkdir -p /app
    cat <<'EOF' > /app/query_oracle
#!/bin/bash
sqlite3 /home/user/data.db "WITH RECURSIVE paths(target_id, depth) AS (
  SELECT target_id, 1 FROM edges WHERE +source_id = $1
  UNION ALL
  SELECT e.target_id, p.depth + 1
  FROM paths p
  JOIN edges e ON +e.source_id = p.target_id
  WHERE p.depth < 3
)
SELECT DISTINCT n.name
FROM paths p
JOIN nodes n ON n.id = p.target_id
ORDER BY n.name ASC;"
EOF
    chmod +x /app/query_oracle

    chmod -R 777 /home/user