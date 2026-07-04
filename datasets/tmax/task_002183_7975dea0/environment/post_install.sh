apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        golang \
        libgl1 \
        libglib2.0-0 \
        sqlite3

    pip3 install pytest opencv-python-headless numpy pandas

    mkdir -p /app

    cat << 'EOF' > /tmp/gen_data.py
import cv2
import numpy as np
import random
import pandas as pd
import os

os.makedirs('/app', exist_ok=True)
nodes = {1:0, 2:1, 3:1, 4:2, 5:2, 6:3, 7:3}

out = cv2.VideoWriter('/app/sensor_feed.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (100, 100))

records = []
random.seed(42)
for i in range(100):
    if i % 7 == 0:
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        out.write(frame)
        continue

    node = random.choice(list(nodes.keys()))
    parent = nodes[node]
    val = random.randint(10, 100)

    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    frame[:] = [val, parent, node]
    out.write(frame)

    records.append({'frame_idx': i, 'node_id': node, 'parent_id': parent, 'value': val})

out.release()

df = pd.DataFrame(records)

def get_depth(n):
    d = 0
    curr = n
    while nodes[curr] != 0:
        d += 1
        curr = nodes[curr]
    return d

df['depth'] = df['node_id'].apply(get_depth)
df['path_smoothed'] = df['value'] + df['depth']

df = df.sort_values('frame_idx')
df['rolling_avg'] = df.groupby('node_id')['path_smoothed'].transform(lambda x: x.rolling(3, min_periods=1).mean())
df['rolling_avg'] = df['rolling_avg'].round(2)

df[['frame_idx', 'node_id', 'rolling_avg']].to_csv('/tmp/ground_truth.csv', index=False)
EOF

    python3 /tmp/gen_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app