apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest opencv-python-headless numpy pandas pyarrow scipy

mkdir -p /app

# Generate the dummy video file
cat << 'EOF' > /tmp/gen_video.py
import cv2
import numpy as np

out = cv2.VideoWriter('/app/factory_feed.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (100, 100))
np.random.seed(0)
for i in range(150):
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    out.write(frame)
out.release()
EOF
python3 /tmp/gen_video.py
rm /tmp/gen_video.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app