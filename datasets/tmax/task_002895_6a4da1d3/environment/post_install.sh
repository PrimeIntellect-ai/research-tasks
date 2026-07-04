apt-get update && apt-get install -y python3 python3-pip ffmpeg golang-go gcc
    pip3 install pytest

    mkdir -p /app
    mkdir -p /tmp/frames

    # Generate a mock video
    ffmpeg -f lavfi -i "testsrc=duration=5:size=128x96:rate=1" -c:v libx264 -pix_fmt yuv420p /app/traffic_feed.mp4

    # Extract frames to calculate their MD5s
    ffmpeg -i /app/traffic_feed.mp4 -r 1 /tmp/frames/frame_%03d.jpg

    # Create the raw and golden CSV files using Python to handle encodings
    cat << 'EOF' > /tmp/setup_csv.py
import os
import hashlib

frames_dir = '/tmp/frames'
raw_csv = '/app/raw_telemetry.csv'
golden_csv = '/tmp/golden_telemetry.csv'

md5s = []
for f in sorted(os.listdir(frames_dir)):
    if f.endswith('.jpg'):
        with open(os.path.join(frames_dir, f), 'rb') as img:
            md5s.append(hashlib.md5(img.read()).hexdigest())

unique_md5s = list(set(md5s))

locations = [
    ("M\xfcnchen", "München"),
    ("S\xe3o Paulo", "São Paulo"),
    ("Paris", "Paris")
]

with open(raw_csv, 'wb') as f_raw, open(golden_csv, 'w', encoding='utf-8') as f_gold:
    for i, md5 in enumerate(unique_md5s):
        loc_cp1252, loc_utf8 = locations[i % len(locations)]
        count = (i + 1) * 10
        raw_line = f"{md5},{loc_cp1252},{count}\n".encode('windows-1252')
        f_raw.write(raw_line)
        f_gold.write(f"{md5},{loc_utf8},{count}\n")

    # Add a decoy row that shouldn't be matched
    f_raw.write(b"decoy_md5,Berlin,5\n")
EOF

    python3 /tmp/setup_csv.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app