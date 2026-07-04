apt-get update && apt-get install -y python3 python3-pip supervisor logrotate
    pip3 install pytest opencv-python-headless pandas numpy

    mkdir -p /app
    mkdir -p /home/user/logs

    # Generate the video and ground truth metrics
    cat << 'EOF' > /tmp/generate_data.py
import cv2
import numpy as np
import pandas as pd

out = cv2.VideoWriter('/app/dashboard_feed.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (100, 100))
records = []
for i in range(120):
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    width = i % 100 + 1
    # BGR format for cv2
    frame[:, :width, 2] = 255 # Red channel
    out.write(frame)
    records.append({'frame': i, 'red_pct': float(width)})
out.release()

df = pd.DataFrame(records)
df.to_csv('/app/ground_truth_metrics.csv', index=False)
EOF
    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user