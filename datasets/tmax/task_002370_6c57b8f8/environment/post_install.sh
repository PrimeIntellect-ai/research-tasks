apt-get update && apt-get install -y python3 python3-pip sqlite3 espeak-ng
    pip3 install pytest

    mkdir -p /app

    # Generate the audio file
    espeak-ng -w /app/incident_report.wav "Attention DBRE team, for the upcoming audit, ensure you only process storage nodes located in the us-west region. I repeat, region must be us-west."

    # Create the SQLite database with the required schema
    sqlite3 /app/backups.db <<EOF
CREATE TABLE clusters (cluster_id INTEGER PRIMARY KEY, cluster_name TEXT);
CREATE TABLE storage_nodes (node_id INTEGER PRIMARY KEY, cluster_id INTEGER, node_name TEXT, region TEXT);
CREATE TABLE backup_logs (log_id INTEGER PRIMARY KEY, node_id INTEGER, database_name TEXT, backup_timestamp DATETIME, backup_size_mb INTEGER, status TEXT);
INSERT INTO clusters (cluster_name) VALUES ('prod-cluster-1');
INSERT INTO storage_nodes (cluster_id, node_name, region) VALUES (1, 'node-a', 'us-west');
INSERT INTO backup_logs (node_id, database_name, backup_timestamp, backup_size_mb, status) VALUES (1, 'users_db', '2023-10-01T12:00:00Z', 1024, 'SUCCESS');
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user