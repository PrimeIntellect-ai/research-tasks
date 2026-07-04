apt-get update && apt-get install -y python3 python3-pip cron libgl1-mesa-glx libglib2.0-0 ffmpeg
    pip3 install --no-cache-dir --default-timeout=100 pytest pandas numpy opencv-python-headless

    mkdir -p /app

    # Create video and reference files
    python3 -c "
import cv2
import numpy as np
import os

# Create 4 frames (0s, 1s, 2s, 3s) at 1 fps
out = cv2.VideoWriter('/app/video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, (100, 100))
colors = [
    [0, 0, 0],       # t=0
    [0, 0, 255],     # t=1 (Red in RGB -> BGR is [0, 0, 255])
    [0, 255, 0],     # t=2 (Green in RGB -> BGR is [0, 255, 0])
    [255, 0, 0],     # t=3 (Blue in RGB -> BGR is [255, 0, 0])
]

for c in colors:
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    frame[:, :] = c
    out.write(frame)
out.release()

# Re-read to get exact averages due to compression
cap = cv2.VideoCapture('/app/video.mp4')

cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
ret, frame1 = cap.read()
b1, g1, r1 = frame1.mean(axis=(0,1))

cap.set(cv2.CAP_PROP_POS_MSEC, 2000)
ret, frame2 = cap.read()
b2, g2, r2 = frame2.mean(axis=(0,1))

with open('/app/reference_features.csv', 'w') as f:
    f.write('frame_id,lang,repaired_text,r_avg,g_avg,b_avg\n')
    f.write(f'1,es,El niño,{r1},{g1},{b1}\n')
    f.write(f'2,fr,C\'est la vie,{r2},{g2},{b2}\n')
"

    # Create broken_loc.jsonl
    cat << 'EOF' > /app/broken_loc.jsonl
{"frame_id": 1, "lang": "es", "raw_text": "El ni\\\\u00f1o"}
{"frame_id": 2, "lang": "fr", "raw_text": "C\\\\u0027est la vie"}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app