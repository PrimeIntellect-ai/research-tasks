apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc make
    pip3 install pytest opencv-python-headless numpy pandas

    mkdir -p /app
    cat << 'EOF' > /tmp/setup.py
import cv2
import numpy as np
import os
import math

os.makedirs('/app', exist_ok=True)
width, height = 640, 360
fps = 30
num_frames = 150

out = cv2.VideoWriter('/app/experiment_monitor.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), isColor=False)
gt_file = open('/tmp/gt.csv', 'w')
gt_file.write("frame,x,y\n")

for i in range(num_frames):
    img = np.zeros((height, width), dtype=np.uint8)

    # Create an artificial drift
    if i < num_frames // 2:
        base_x = 200 + i * 0.5
    else:
        base_x = 400 + (i - num_frames // 2) * 0.5

    y = int(180 + 50 * math.sin(i * 0.1))
    x = int(base_x)

    # Add noise to background
    noise = np.random.randint(0, 30, (height, width), dtype=np.uint8)
    img = cv2.add(img, noise)

    # Draw artifact
    cv2.circle(img, (x, y), 5, (255), -1)

    out.write(img)
    gt_file.write(f"{i},{x},{y}\n")

out.release()
gt_file.close()
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user