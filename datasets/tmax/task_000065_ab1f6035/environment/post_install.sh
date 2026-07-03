apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest "numpy<2.0.0" opencv-python-headless pandas pyarrow

    python3 -c "
import cv2
import numpy as np
import json
import os

os.makedirs('/app', exist_ok=True)

num_frames = 300
width, height = 320, 240
fps = 30

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/sensor_feed.mp4', fourcc, fps, (width, height))

np.random.seed(42)
signals = []

with open('/app/metadata.jsonl', 'w') as f, open('/app/ground_truth.csv', 'w') as gt:
    gt.write('frame_index,signal\n')
    for i in range(num_frames):
        signal_val = int(np.random.randint(50, 200))
        signals.append(signal_val)

        frame = np.zeros((height, width, 3), dtype=np.uint8)
        cx, cy = width // 2, height // 2
        frame[cy-32:cy+32, cx-32:cx+32] = (signal_val, signal_val, signal_val)

        out.write(frame)

        ts = f'2024-01-01T00:00:{i:02d}Z'
        f.write(json.dumps({'frame_index': i, 'timestamp': ts}) + '\n')

        gt.write(f'{i},{signal_val}\n')

out.release()
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user