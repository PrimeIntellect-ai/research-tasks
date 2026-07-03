apt-get update && apt-get install -y python3 python3-pip ffmpeg cargo python3-opencv python3-numpy
pip3 install pytest

mkdir -p /app
cat << 'EOF' > /app/generate_video.py
#!/usr/bin/env python3
import cv2
import numpy as np
import random

out = cv2.VideoWriter('/app/legacy_dashboard.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, (640, 480))
random.seed(42)

for i in range(60):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    is_active = random.choice([True, False])
    if is_active:
        frame[:, :] = (0, 0, 255)
    else:
        frame[:, :] = (255, 0, 0)
    out.write(frame)
out.release()
EOF
python3 /app/generate_video.py

useradd -m -s /bin/bash user || true

cat << 'EOF' > /home/user/init_routing.sh
#!/bin/bash
mkdir -p /home/user/routing_rules
chmod 755 /home/user/routing_rules
EOF
chmod +x /home/user/init_routing.sh

cat << 'EOF' > /home/user/startup.sh
#!/bin/bash
/home/user/init_routing.sh &
echo "Starting downstream router..."
EOF
chmod +x /home/user/startup.sh

chmod -R 777 /home/user