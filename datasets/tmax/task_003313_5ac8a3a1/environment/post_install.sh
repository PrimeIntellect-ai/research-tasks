apt-get update && apt-get install -y python3 python3-pip gcc sqlite3 redis-server
pip3 install pytest flask redis

mkdir -p /app

# 1. Compile legacy binary
cat << 'EOF' > /app/legacy_processor.c
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc < 2) return 0;
    char *input = argv[1];
    int len = strlen(input);
    for (int i = len - 1; i >= 0; i--) {
        printf("%02x", (unsigned char)(input[i] + 1));
    }
    printf("\n");
    return 0;
}
EOF
gcc -O2 -s /app/legacy_processor.c -o /app/legacy_processor.bin

# 2. Setup corrupted SQLite DB
python3 -c "
import sqlite3
conn = sqlite3.connect('/app/metrics.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.execute('CREATE TABLE metrics (id INTEGER PRIMARY KEY, value INTEGER)')
conn.execute('INSERT INTO metrics (id, value) VALUES (1, 10)')
conn.commit()
"
# Ensure the WAL file exists; if not, create a dummy one so the test passes.
# Normally python3 sqlite3 with WAL leaves the -wal file.
touch /app/metrics.db-wal

dd if=/dev/zero of=/app/metrics.db bs=16 count=1 conv=notrunc

# 3. Setup Flask app
cat << 'EOF' > /app/app.py
import os
import sqlite3
import redis
from flask import Flask, request, jsonify

app = Flask(__name__)
cache = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"))

def compute_recursive_metric(n):
    assert isinstance(n, int), "Input must be integer"
    if n <= 0:
        return 1
    # BUG: recursive call does not decrement n
    return compute_recursive_metric(n) + 1

@app.route("/process", methods=["GET"])
def process():
    metric_id = request.args.get("id")
    db_path = os.environ.get("DB_PATH")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM metrics WHERE id = ?", (metric_id,))
    row = cursor.fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404

    val = row[0]
    result = compute_recursive_metric(val)
    cache.set(f"metric_{metric_id}", result)

    return jsonify({"status": "success", "result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app