apt-get update && apt-get install -y python3 python3-pip tesseract-ocr
    pip3 install pytest Pillow

    mkdir -p /app

    # Generate config.png
    cat << 'EOF' > /app/generate_image.py
from PIL import Image, ImageDraw
img = Image.new('RGB', (300, 100), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10, 10), "Window: 15\nBandwidth: 0.12", fill=(0, 0, 0))
img.save('/app/config.png')
EOF
    python3 /app/generate_image.py
    rm /app/generate_image.py

    # Create oracle.py
    cat << 'EOF' > /app/oracle.py
#!/usr/bin/env python3
import sys, math
seq = sys.stdin.read().strip()
W = 15
h = 0.12
if len(seq) < W:
    print("INVALID")
    sys.exit(0)
gcs = []
for i in range(len(seq) - W + 1):
    window = seq[i:i+W]
    gcs.append((window.count('G') + window.count('C')) / W)
targets = [0.1, 0.3, 0.5, 0.7, 0.9]
out = []
for x in targets:
    val = sum(math.exp(-((x - gc)**2) / (2 * h**2)) for gc in gcs)
    out.append(f"{val:.4f}")
print(",".join(out))
EOF
    chmod +x /app/oracle.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user