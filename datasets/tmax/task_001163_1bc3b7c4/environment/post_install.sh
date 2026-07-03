apt-get update && apt-get install -y python3 python3-pip jq tar util-linux
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    echo "server_id,timestamp,backup_size" > /home/user/backup_summary.csv

    cat << 'EOF' > /home/user/data.json
[
  {"server_id": "srv-01", "timestamp": "2023-10-01T12:00:00Z", "backup_size": 1048576, "status": "success"},
  {"server_id": "srv-02", "timestamp": "2023-10-01T12:05:00Z", "backup_size": 2048576, "status": "success"},
  {"server_id": "srv-03", "timestamp": "2023-10-01T12:10:00Z", "backup_size": 512000, "status": "failed"}
]
EOF

    tar -czf /home/user/incoming_backup.tar.gz -C /home/user data.json
    rm /home/user/data.json

    chmod -R 777 /home/user