apt-get update && apt-get install -y python3 python3-pip wget tar ffmpeg
pip3 install pytest opencv-python-headless numpy

# Install Go
wget -q https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz
rm go1.21.6.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

# Generate the video
mkdir -p /app
cat << 'EOF' > /tmp/gen_video.py
import cv2
import numpy as np
import os

os.makedirs("/app", exist_ok=True)

width, height = 200, 200
fps = 10
frames = 60

A = np.array([[0.98, 0.05],
              [-0.05, 0.98]])

X = np.array([100.0, 50.0]) # Starting position

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/movement.mp4', fourcc, fps, (width, height))

for t in range(frames):
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Draw particle
    x, y = int(round(X[0])), int(round(X[1]))
    if 0 <= x < width and 0 <= y < height:
        cv2.circle(img, (x, y), 3, (255, 255, 255), -1)

    out.write(img)

    # Update position
    X = A @ X

out.release()
EOF

python3 /tmp/gen_video.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app