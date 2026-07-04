apt-get update && apt-get install -y python3 python3-pip libgl1 libglib2.0-0 libzbar0
    pip3 install pytest opencv-python qrcode pillow numpy pandas scikit-learn pyzbar

    mkdir -p /app

    cat << 'EOF' > /tmp/gen.py
import cv2
import qrcode
import numpy as np
import random
import csv

random.seed(42)
nodes = ['Alpha', 'Beta', 'Gamma']
frames = 100
fps = 10

out = cv2.VideoWriter('/app/network_traffic.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (256, 256))

gt_data = []
for i in range(frames):
    src = random.choice(nodes)
    dst = random.choice([n for n in nodes if n != src])
    bytes_val = random.randint(10, 500)

    text = f"{src},{dst},{bytes_val}"
    gt_data.append((i, src, dst, bytes_val))

    qr = qrcode.make(text).convert('RGB')
    img = np.array(qr)
    img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_NEAREST)
    out.write(img)

out.release()

# Generate ground truth results
history = {n: [0]*frames for n in nodes}
for f, s, d, b in gt_data:
    history[d][f] = b

with open('/tmp/ground_truth_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['frame_id', 'destination', 'rolling_bytes'])
    for frame_id, s, d, b in gt_data:
        # window: current and 2 preceding
        window_sum = history[d][frame_id]
        if frame_id >= 1: window_sum += history[d][frame_id-1]
        if frame_id >= 2: window_sum += history[d][frame_id-2]
        writer.writerow([frame_id, d, window_sum])
EOF

    python3 /tmp/gen.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app /tmp/ground_truth_results.csv