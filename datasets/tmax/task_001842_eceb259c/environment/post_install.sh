apt-get update && apt-get install -y python3 python3-pip ffmpeg
pip3 install pytest pandas numpy

mkdir -p /app/data

cat << 'EOF' > /tmp/setup.py
import os
import json
import random
import numpy as np
import pandas as pd
import subprocess

# Generate video
os.makedirs('/app/data', exist_ok=True)
fps = 30
duration = 60
total_frames = fps * duration

# Create raw frames
frames = np.zeros((total_frames, 100, 100, 3), dtype=np.uint8)
frames[:, :, :] = [255, 255, 255] # White background

# Red indicator at seconds 10, 40, 41
frames[10*fps:11*fps, 0:10, 0:10] = [255, 0, 0] # Red (RGB)
frames[40*fps:42*fps, 0:10, 0:10] = [255, 0, 0]

# Write video using ffmpeg
process = subprocess.Popen([
    'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
    '-s', '100x100', '-pix_fmt', 'rgb24', '-r', str(fps),
    '-i', '-', '-c:v', 'libx264', '-preset', 'ultrafast',
    '-pix_fmt', 'yuv420p', '/app/deploy_dashboard.mp4'
], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
process.communicate(frames.tobytes())

# Generate events
random.seed(42)
events = []
services = ['A', 'B', 'C']

num_events = 50000
for i in range(num_events):
    t = random.uniform(0, 60)
    sid = random.choice(services)
    h = f"hash_{random.randint(1, 1000)}"
    size = random.randint(10, 1000)
    events.append({'timestamp': t, 'service_id': sid, 'config_hash': h, 'payload_size': size})

# Inject duplicates
for t_start in [10, 40, 41]:
    for _ in range(50):
        t = random.uniform(t_start, t_start + 0.999)
        sid = random.choice(services)
        h = f"hash_{random.randint(1, 10)}" # likely to be seen
        events.append({'timestamp': t, 'service_id': sid, 'config_hash': h, 'payload_size': random.randint(10, 1000)})

events.sort(key=lambda x: x['timestamp'])

with open('/app/data/config_events.jsonl', 'w') as f:
    for e in events:
        f.write(json.dumps(e) + '\n')

# Process events for ground truth
retry_seconds = {10, 40, 41}
clean_events = []
seen = set()

for e in events:
    t = e['timestamp']
    sec = int(t)
    sid = e['service_id']
    h = e['config_hash']

    is_dup = False
    if sec in retry_seconds:
        if (sid, h) in seen:
            is_dup = True

    if not is_dup:
        clean_events.append(e)

    seen.add((sid, h))

# Calculate rolling sum
rolling_sizes = []
for T in range(60):
    window_sum = 0
    for e in clean_events:
        if T - 4 < e['timestamp'] <= T:
            window_sum += e['payload_size']
    rolling_sizes.append({'second': T, 'rolling_size': window_sum})

pd.DataFrame(rolling_sizes).to_csv('/app/ground_truth_metrics.csv', index=False)
EOF

python3 /tmp/setup.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app