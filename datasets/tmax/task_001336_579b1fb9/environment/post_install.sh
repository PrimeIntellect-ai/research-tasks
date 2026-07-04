apt-get update && apt-get install -y python3 python3-pip ffmpeg
pip3 install pytest numpy opencv-python-headless scipy imageio imageio-ffmpeg

# Create /app directory
mkdir -p /app
cd /app

# Write oracle simulator
cat << 'EOF' > /app/oracle_simulator
#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--x0', type=float, required=True)
parser.add_argument('--v0', type=float, required=True)
parser.add_argument('--steps', type=int, required=True)
args = parser.parse_args()

k = 6.42
c = 0.75
dt = 1/30.0

x = args.x0
v = args.v0

for _ in range(args.steps):
    x_new = x + v * dt
    v_new = v + (-k * x - c * v) * dt
    x = x_new
    v = v_new

print(f"{x:.4f}")
EOF
chmod +x /app/oracle_simulator

# Generate video
cat << 'EOF' > /tmp/gen_video.py
import numpy as np
import cv2

k = 6.42
c = 0.75
dt = 1/30.0
x = 15.0
v = 0.0

frames = 150 # 5 seconds
width = 640
height = 480
fps = 30

out = cv2.VideoWriter('/app/oscillator.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

for _ in range(frames):
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Calculate pixel position
    px = int(320 + x * 10)
    py = 240

    # Draw 5x5 white square
    if 0 <= px-2 and px+2 < width:
        img[py-2:py+3, px-2:px+3] = (255, 255, 255)

    out.write(img)

    # Update state
    x_new = x + v * dt
    v_new = v + (-k * x - c * v) * dt
    x = x_new
    v = v_new

out.release()
EOF
python3 /tmp/gen_video.py

# Setup user
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user