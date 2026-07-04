apt-get update && apt-get install -y python3 python3-pip ffmpeg cargo libsm6 libxext6
    pip3 install pytest pandas numpy scikit-learn opencv-python-headless

    mkdir -p /app
    # Generate a 65-second dummy video
    ffmpeg -f lavfi -i testsrc=duration=65:size=320x240:rate=30 -c:v libx264 /app/video.mp4

    # Generate ground truth
    cat << 'EOF' > /tmp/gen_gt.py
import os
import cv2
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances

os.makedirs('/tmp/frames_gt', exist_ok=True)
os.system('ffmpeg -i /app/video.mp4 -vf fps=1 /tmp/frames_gt/frame_%04d.jpg -hide_banner -loglevel error')

frames = sorted([f for f in os.listdir('/tmp/frames_gt') if f.endswith('.jpg')])
data = []
is_valid = []

for f in frames:
    img = cv2.imread(os.path.join('/tmp/frames_gt', f), cv2.IMREAD_GRAYSCALE)
    avg = np.mean(img)
    if avg < 10.0:
        data.append(np.full(64, np.nan))
        is_valid.append(False)
    else:
        hist, _ = np.histogram(img, bins=64, range=(0, 256))
        hist = hist.astype(float) / np.sum(hist)
        data.append(hist)
        is_valid.append(True)

data = np.array(data)

for i in range(len(data)):
    if not is_valid[i]:
        prev_idx = i - 1
        while prev_idx >= 0 and not is_valid[prev_idx]:
            prev_idx -= 1
        next_idx = i + 1
        while next_idx < len(data) and not is_valid[next_idx]:
            next_idx += 1

        if prev_idx >= 0 and next_idx < len(data):
            data[i] = (data[prev_idx] + data[next_idx]) / 2.0
        elif prev_idx >= 0:
            data[i] = data[prev_idx]
        elif next_idx < len(data):
            data[i] = data[next_idx]
        else:
            data[i] = np.zeros(64)

pca = PCA(n_components=4, random_state=42)
data_pca = pca.fit_transform(data)

dist = pairwise_distances(data_pca)
np.fill_diagonal(dist, np.inf)

queries = [10, 20, 30, 40, 50]
res = []
for q in queries:
    idx = q - 1
    if idx < len(dist):
        top5 = np.argsort(dist[idx])[:5] + 1
        res.append([q] + list(top5))

df = pd.DataFrame(res, columns=['query_frame', 'sim_1', 'sim_2', 'sim_3', 'sim_4', 'sim_5'])
df.to_csv('/tmp/ground_truth.csv', index=False)
EOF

    python3 /tmp/gen_gt.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user