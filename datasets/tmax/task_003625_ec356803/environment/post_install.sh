apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest numpy opencv-python-headless

    mkdir -p /app
    mkdir -p /home/user/artifact_store

    cat << 'EOF' > /app/setup.py
import os
import random
import cv2
import numpy as np

random.seed(42)

valid_ids = []

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/artifact_feed.mp4', fourcc, 30.0, (640, 480))

with open('/home/user/artifact_meta.log', 'w') as f_log:
    for i in range(600):
        art_id = f"art_{i:03d}"
        art_dir = f"/home/user/artifact_store/{art_id}"
        os.makedirs(art_dir, exist_ok=True)

        is_loop = random.random() < 0.2
        is_deprecated = random.random() < 0.2
        is_red = random.random() < 0.2

        if is_loop:
            os.symlink('.', os.path.join(art_dir, 'loop'))

        status = "DEPRECATED" if is_deprecated else "ACTIVE"
        f_log.write(f"[Artifact: {art_id}]\n")
        f_log.write(f"Author: dev_team\n")
        f_log.write(f"Checksum: 8a9d...\n")
        f_log.write(f"Status: {status}\n")
        f_log.write(f"---\n")

        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        if is_red:
            frame[0:50, 0:50] = [0, 0, 255] # OpenCV uses BGR
        else:
            frame[0:50, 0:50] = [255, 0, 0] # Blue

        out.write(frame)

        if not is_loop and not is_deprecated and not is_red:
            valid_ids.append(art_id)

out.release()

with open('/app/ground_truth_valid.txt', 'w') as f_gt:
    for v in valid_ids:
        f_gt.write(v + '\n')
EOF

    python3 /app/setup.py
    rm /app/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app