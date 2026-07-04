apt-get update && apt-get install -y python3 python3-pip postgresql redis-server sudo
    pip3 install pytest psycopg2-binary redis

    mkdir -p /app

    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
service postgresql start
service redis-server start

su - postgres -c "psql -c \"CREATE USER etl_user WITH PASSWORD 'etl_password';\"" || true
su - postgres -c "psql -c \"CREATE DATABASE etl_db OWNER etl_user;\"" || true

su - postgres -c "psql -d etl_db -c \"CREATE TABLE IF NOT EXISTS transfers (id SERIAL PRIMARY KEY, src INT, dst INT, amount INT, ts TIMESTAMP);\""

# Insert some dummy data
su - postgres -c "psql -d etl_db -c \"INSERT INTO transfers (src, dst, amount, ts) SELECT floor(random() * 1000 + 1)::int, floor(random() * 1000 + 1)::int, floor(random() * 10000)::int, NOW() - (random() * interval '365 days') FROM generate_series(1, 50000);\""
EOF
    chmod +x /app/start_services.sh

    cat << 'EOF' > /app/oracle_query
#!/usr/bin/env python3
import sys
import json
import psycopg2

def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    user_id = int(sys.argv[1])

    conn = psycopg2.connect(dbname="etl_db", user="etl_user", password="etl_password", host="localhost")
    cur = conn.cursor()

    # degree
    cur.execute("""
        SELECT COUNT(DISTINCT other) FROM (
            SELECT dst AS other FROM transfers WHERE src = %s
            UNION
            SELECT src AS other FROM transfers WHERE dst = %s
        ) t
    """, (user_id, user_id))
    degree = cur.fetchone()[0]

    # mutual_volume
    cur.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM transfers t1
        WHERE t1.src = %s AND EXISTS (
            SELECT 1 FROM transfers t2 WHERE t2.src = t1.dst AND t2.dst = %s
        )
    """, (user_id, user_id))
    mutual_volume = int(cur.fetchone()[0])

    # max_rolling_3
    cur.execute("""
        WITH ordered AS (
            SELECT amount, ROW_NUMBER() OVER (ORDER BY ts) as rn
            FROM transfers WHERE src = %s
        )
        SELECT COALESCE(MAX(rolling_sum), 0) FROM (
            SELECT amount + 
                   COALESCE(LAG(amount, 1) OVER (ORDER BY rn), 0) + 
                   COALESCE(LAG(amount, 2) OVER (ORDER BY rn), 0) as rolling_sum
            FROM ordered
        ) sub
    """, (user_id,))
    res = cur.fetchone()
    max_rolling_3 = int(res[0]) if res and res[0] is not None else 0

    print(json.dumps({
        "degree": degree,
        "mutual_volume": mutual_volume,
        "max_rolling_3": max_rolling_3
    }))

if __name__ == "__main__":
    main()
EOF
    chmod +x /app/oracle_query

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user