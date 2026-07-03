apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest opencv-python-headless numpy pandas

    cat << 'EOF' > /tmp/setup.py
import cv2
import numpy as np
import pandas as pd
import os

os.makedirs('/app', exist_ok=True)

# Generate /app/experiment.mp4
width, height = 100, 100
fps = 10
duration = 5 # 50 frames
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/experiment.mp4', fourcc, fps, (width, height))

np.random.seed(42)
intensities = []
for i in range(fps * duration):
    # Base intensity between 50 and 200
    base = int(np.random.randint(50, 200))
    frame = np.full((height, width, 3), base, dtype=np.uint8)
    # Add some noise
    noise = np.random.randint(-10, 10, (height, width, 3), dtype=np.int16)
    frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    out.write(frame)
    # the grayscale mean will be roughly 'base'
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    intensities.append(int(np.round(gray.mean())))

out.release()

# Generate /app/history.csv
num_rows = 1_000_000
timestamps = pd.date_range(start='2020-01-01', periods=num_rows, freq='S')
categories = np.random.choice(['A', 'B', 'C', 'D'], num_rows)
intensity_vals = np.random.randint(0, 256, num_rows)
location_ids = np.random.randint(1, 100, num_rows)

df = pd.DataFrame({
    'event_id': range(1, num_rows + 1),
    'timestamp': timestamps,
    'intensity': intensity_vals,
    'category': categories,
    'location_id': location_ids
})

df.to_csv('/app/history.csv', index=False)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user