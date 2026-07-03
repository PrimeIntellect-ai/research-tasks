apt-get update && apt-get install -y python3 python3-pip sqlite3 jq
    pip3 install pytest

    mkdir -p /home/user/data

    cat << 'EOF' > /home/user/data/nodes.json
[
  {"id": "node_01", "role": "gateway", "active": true},
  {"id": "node_02", "role": "relay", "active": true},
  {"id": "node_03", "role": "relay", "active": true},
  {"id": "node_04", "role": "relay", "active": true},
  {"id": "node_05", "role": "relay", "active": true},
  {"id": "node_06", "role": "master_db", "active": true}
]
EOF

    sqlite3 /home/user/data/graph.db << 'EOF'
CREATE TABLE edges (source TEXT, target TEXT, is_deleted INTEGER);
-- Shortest path but it's deleted (1 hop)
INSERT INTO edges VALUES ('node_01', 'node_06', 1);

-- Another deleted short path (2 hops)
INSERT INTO edges VALUES ('node_01', 'node_05', 0);
INSERT INTO edges VALUES ('node_05', 'node_06', 1);

-- The actual shortest valid path (3 hops)
INSERT INTO edges VALUES ('node_01', 'node_02', 0);
INSERT INTO edges VALUES ('node_02', 'node_03', 0);
INSERT INTO edges VALUES ('node_03', 'node_06', 0);

-- Distractor path (4 hops)
INSERT INTO edges VALUES ('node_01', 'node_04', 0);
INSERT INTO edges VALUES ('node_04', 'node_05', 0);
INSERT INTO edges VALUES ('node_05', 'node_03', 0);
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user