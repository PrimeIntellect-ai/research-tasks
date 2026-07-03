apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas numpy opencv-python-headless rdflib

    mkdir -p /app

    # Generate a dummy video for testing
    cat << 'EOF' > /app/generate_video.py
import cv2
import numpy as np

out = cv2.VideoWriter('/app/experiment_record.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (100, 100))
for i in range(30):
    # Create frames with varying intensity
    intensity = (i * 10) % 255
    frame = np.full((100, 100, 3), intensity, dtype=np.uint8)
    out.write(frame)
out.release()
EOF
    python3 /app/generate_video.py
    rm /app/generate_video.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app