apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest Pillow opencv-python-headless

    mkdir -p /app

    cat << 'EOF' > /tmp/setup.py
import csv
import random
from PIL import Image
import os
import subprocess

# Generate edges.csv
with open('/app/edges.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['src', 'dst', 'cost'])
    for i in range(100):
        for j in range(100):
            if i != j and random.random() < 0.2:
                writer.writerow([i, j, round(random.uniform(1.0, 10.0), 2)])

# Generate frames
for t in range(60):
    img = Image.new('RGB', (100, 100), color='white')
    pixels = img.load()
    offline_nodes = random.sample(range(100), random.randint(10, 20))
    for node in offline_nodes:
        r = node // 10
        c = node % 10
        for i in range(10):
            for j in range(10):
                pixels[c*10 + j, r*10 + i] = (0, 0, 0)
    img.save(f'/tmp/frame_{t:02d}.png')

subprocess.run(['ffmpeg', '-framerate', '1', '-i', '/tmp/frame_%02d.png', '-c:v', 'libx264', '-qp', '0', '/app/node_status.mp4'], check=True)
EOF

    python3 /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app