apt-get update && apt-get install -y python3 python3-pip python3-opencv python3-numpy python3-networkx
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /tmp/setup.py
import sqlite3
import cv2
import numpy as np
import os

os.makedirs('/app', exist_ok=True)

# 1. Generate Video
fps = 30
duration = 10
total_frames = fps * duration
width, height = 200, 200

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/network_traffic.mp4', fourcc, fps, (width, height))

flash_frames = [45, 120, 210, 250] # Timestamps: 1.5, 4.0, 7.0, 8.333

for i in range(total_frames):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    if i in flash_frames:
        frame[0:50, 0:50] = (255, 255, 255)
    out.write(frame)
out.release()

# 2. Generate Database
conn = sqlite3.connect('/app/network.db')
c = conn.cursor()

c.execute("PRAGMA writable_schema = 1")
c.execute("CREATE TABLE event_logs (id INTEGER PRIMARY KEY, event_time REAL, source_node TEXT, target_node TEXT, payload_size REAL)")
c.execute("CREATE INDEX idx_time ON event_logs(event_time)")

events = [
    (1.505, 'NODE_A', 'NODE_B', 100),
    (1.502, 'NODE_A', 'NODE_C', 250),
    (4.010, 'NODE_B', 'NODE_D', 150),
    (4.000, 'NODE_C', 'NODE_D', 50),
    (7.005, 'NODE_D', 'NODE_Z', 200),
    (8.333, 'NODE_C', 'NODE_Z', 500)
]

for ev in events:
    c.execute("INSERT INTO event_logs (event_time, source_node, target_node, payload_size) VALUES (?, ?, ?, ?)", ev)

# Insert noise
for i in range(100):
    c.execute("INSERT INTO event_logs (event_time, source_node, target_node, payload_size) VALUES (?, ?, ?, ?)", (i*0.1, 'NODE_X', 'NODE_Y', 10))

conn.commit()
conn.close()
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app