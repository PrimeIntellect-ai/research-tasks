apt-get update && apt-get install -y python3 python3-pip ffmpeg g++
    pip3 install pytest

    mkdir -p /app
    ffmpeg -f lavfi -i testsrc=duration=10:size=640x480:rate=30 -c:v libx264 /app/experiment_run.mp4

    cat << 'EOF' > /app/reference_organizer_src.py
import sys, re
for line in sys.stdin:
    line = line.strip()
    match = re.search(r'([0-9]{6})\.jpg$', line)
    if not match:
        print("ACTION: IGNORE")
        continue

    frame_id = int(match.group(1))
    filename = line.replace('/', '_')

    if frame_id % 5 == 0:
        print(f"ACTION: HARDLINK, TARGET: val_set/val_{filename}")
    else:
        print(f"ACTION: SYMLINK, TARGET: train_set/train_{filename}")
EOF
    chmod +x /app/reference_organizer_src.py

    cat << 'EOF' > /app/reference_organizer
#!/bin/bash
python3 /app/reference_organizer_src.py
EOF
    chmod +x /app/reference_organizer

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user