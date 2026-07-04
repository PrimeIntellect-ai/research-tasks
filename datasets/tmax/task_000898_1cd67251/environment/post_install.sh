apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install required packages
    apt-get install -y imagemagick sqlite3 libsqlite3-dev tesseract-ocr g++

    mkdir -p /app
    cd /app

    # Create the dashboard image
    convert -size 400x200 xc:white -font DejaVu-Sans -pointsize 18 -fill black \
    -draw "text 10,30 'Dashboard Configuration'" \
    -draw "text 10,60 'Target Sensor: SENS-404'" \
    -draw "text 10,90 'Status Filter: CRITICAL'" \
    -draw "text 10,120 'Order: timestamp DESC'" \
    -draw "text 10,150 'Limit: 20'" \
    /app/query_spec.png

    # Create the SQLite database
    cat << 'EOF' > /app/setup_db.py
import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('/app/sensor_data.db')
cursor = conn.cursor()

cursor.execute('CREATE TABLE readings (id INTEGER PRIMARY KEY, sensor_id TEXT, timestamp DATETIME, value REAL, status TEXT)')
cursor.execute('CREATE INDEX idx_sensor_time ON readings(sensor_id, timestamp)')

sensors = ['SENS-101', 'SENS-202', 'SENS-404']
statuses = ['OK', 'WARNING', 'CRITICAL']

start_time = datetime(2023, 1, 1)

rows = []
for i in range(1, 1001):
    sensor = random.choice(sensors)
    # Ensure we have enough SENS-404 CRITICAL
    if i % 5 == 0:
        sensor = 'SENS-404'
        status = 'CRITICAL'
    else:
        status = random.choice(statuses)

    ts = start_time + timedelta(minutes=i)
    val = round(random.uniform(10.0, 99.9), 2)
    rows.append((i, sensor, ts.strftime('%Y-%m-%d %H:%M:%S'), val, status))

cursor.executemany('INSERT INTO readings VALUES (?, ?, ?, ?, ?)', rows)
conn.commit()

# For verifiable truth, we will just generate the golden dataset.
cursor.execute("SELECT id FROM readings WHERE sensor_id='SENS-404' AND status='CRITICAL' ORDER BY timestamp DESC LIMIT 20")
golden_ids = [str(row[0]) for row in cursor.fetchall()]

with open('/app/golden_ids.txt', 'w') as f:
    f.write(','.join(golden_ids))

conn.close()
EOF
    python3 /app/setup_db.py

    # Create the verifier
    cat << 'EOF' > /app/verifier.py
import sys
import os

if not os.path.exists('/home/user/results.csv'):
    print("Metric: 0.0")
    sys.exit(0)

with open('/app/golden_ids.txt', 'r') as f:
    expected = set(f.read().strip().split(','))

actual = set()
with open('/home/user/results.csv', 'r') as f:
    lines = f.readlines()
    if len(lines) > 1:
        for line in lines[1:]: # skip header
            parts = line.strip().split(',')
            if len(parts) > 0:
                actual.add(parts[0])

if not expected or not actual:
    print("Metric: 0.0")
    sys.exit(0)

intersection = expected.intersection(actual)
union = expected.union(actual)
jaccard = len(intersection) / len(union)

print(f"Metric: {jaccard}")
EOF
    chmod +x /app/verifier.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user