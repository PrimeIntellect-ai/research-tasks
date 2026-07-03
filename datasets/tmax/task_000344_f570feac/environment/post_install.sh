apt-get update && apt-get install -y python3 python3-pip python3-opencv
pip3 install pytest

mkdir -p /app

cat << 'EOF' > /tmp/gen_video.py
import cv2
import numpy as np
import sys

text = "MODE=PRODUCTION"
bits = ''.join(format(ord(c), '08b') for c in text)

out = cv2.VideoWriter('/app/telemetry.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (64, 64), isColor=False)
if not out.isOpened():
    print("Failed to open VideoWriter")
    sys.exit(1)

for bit in bits:
    color = 255 if bit == '1' else 0
    frame = np.full((64, 64), color, dtype=np.uint8)
    out.write(frame)

out.release()
EOF

python3 /tmp/gen_video.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app