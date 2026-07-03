apt-get update && apt-get install -y python3 python3-pip postgresql redis-server curl sudo
    pip3 install pytest psycopg2-binary redis requests flask

    mkdir -p /home/user/workspace
    mkdir -p /app/flask_service

    cat << 'EOF' > /app/flask_service/config.env
REDIS_PORT=6380
PG_PORT=5433
EOF

    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
service postgresql start
service redis-server start
# Initialize DB and Redis if needed
su - postgres -c "psql -c \"CREATE USER user WITH SUPERUSER PASSWORD 'user';\"" || true
su - postgres -c "createdb db" || true
EOF
    chmod +x /app/start_services.sh

    cat << 'EOF' > /app/oracle_planner
#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--db-id', type=int)
args = parser.parse_args()
print(f"s3://backups/db/{args.db_id}/chunk1")
EOF
    chmod +x /app/oracle_planner

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user