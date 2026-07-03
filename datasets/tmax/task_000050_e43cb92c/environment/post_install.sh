apt-get update && apt-get install -y python3 python3-pip python3-opencv python3-numpy
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /app/generate.py
import json
import base64
import urllib.parse
import cv2
import numpy as np

events = []
ground_truth = {}
np.random.seed(42)

for i in range(1, 101):
    is_malicious = np.random.choice([0, 1])
    ground_truth[str(i)] = int(is_malicious)

    if is_malicious:
        # Generate various path traversals
        traversals = ["../", "..%2f", "%2e%2e%2f", "%252e%252e%252f", "..\\", "%2e%2e\\"]
        base = np.random.choice(traversals) * np.random.randint(2, 5)
        filename = f"{base}etc/passwd"
    else:
        filename = f"image_{i}.jpg"

    req = json.dumps({"filename": filename, "data": "dummy"})
    encoded_payload = base64.b64encode(req.encode()).hex()
    events.append({"id": i, "encoded_payload": encoded_payload})

json_str = json.dumps(events)
bitstream = ''.join(format(ord(c), '08b') for c in json_str)

# Generate video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/traffic_pulses.mp4', fourcc, 30.0, (10, 10))

for bit in bitstream:
    color = 255 if bit == '1' else 0
    frame = np.full((10, 10, 3), color, dtype=np.uint8)
    out.write(frame)

out.release()

with open('/app/ground_truth.json', 'w') as f:
    json.dump(ground_truth, f)
EOF

    python3 /app/generate.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app