apt-get update && apt-get install -y python3 python3-pip tesseract-ocr golang
    pip3 install pytest numpy pillow

    mkdir -p /app /home/user

    cat << 'EOF' > /tmp/setup.py
import csv
import numpy as np
from PIL import Image, ImageDraw
import os

os.makedirs("/app", exist_ok=True)
img = Image.new('RGB', (400, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = "PRIOR_MEAN=50.0\nPRIOR_VAR=25.0\nPORT=8123"
d.text((10,10), text, fill=(0,0,0))
img.save('/app/config.png')

np.random.seed(42)
valid_data = np.random.normal(48.0, 5.0, 90).tolist()
missing_data = ["NaN", "", "NaN", ""]
outlier_data = [-10.5, 105.2, 110.0]
all_data = valid_data + missing_data + outlier_data
np.random.shuffle(all_data)

with open('/home/user/sensor_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "value"])
    for i, val in enumerate(all_data):
        writer.writerow([i+1, val])
EOF

    python3 /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user