apt-get update && apt-get install -y python3 python3-pip cargo rustc ffmpeg
    pip3 install pytest opencv-python-headless numpy

    cat << 'EOF' > /tmp/setup.py
import cv2
import numpy as np
import random
import os

os.makedirs('/app', exist_ok=True)

# Ground truth sequence
random.seed(42)
bases = ['A', 'C', 'G', 'T']
truth_seq = "".join(random.choices(bases, k=50))

# Generate Video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/base_calls.mp4', fourcc, 10.0, (100, 100))

quadrants = {
    'A': ((0, 0), (50, 50)),
    'C': ((50, 0), (100, 50)),
    'G': ((0, 50), (50, 100)),
    'T': ((50, 50), (100, 100))
}

for base in truth_seq:
    frame = np.random.randint(0, 50, (100, 100, 3), dtype=np.uint8)
    (x1, y1), (x2, y2) = quadrants[base]
    # Make the correct quadrant bright
    frame[y1:y2, x1:x2] = np.random.randint(200, 255, (50, 50, 3), dtype=np.uint8)
    out.write(frame)

out.release()

# Generate FASTA
with open('/app/dataset.fasta', 'w') as f:
    for i in range(10000):
        if i == 4200:
            # Inject a sequence with 1 mutation
            mutated = list(truth_seq)
            mut_idx = 25
            mutated[mut_idx] = random.choice([b for b in bases if b != truth_seq[mut_idx]])
            f.write(f">SEQ_{i:05d}\n{''.join(mutated)}\n")
        else:
            random_seq = "".join(random.choices(bases, k=50))
            f.write(f">SEQ_{i:05d}\n{random_seq}\n")

with open('/app/truth.txt', 'w') as f:
    f.write(truth_seq)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app