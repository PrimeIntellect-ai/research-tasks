apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest

    mkdir -p /app

    # Create the oracle parser
    cat << 'EOF' > /app/oracle_parser
#!/usr/bin/env python3
import sys
import re

if len(sys.argv) < 2:
    sys.exit(1)
offset = int(sys.argv[1])

for line in sys.stdin:
    line = line.rstrip('\r\n')
    if not line:
        continue
    if line.startswith('#'):
        continue

    match = re.fullmatch(r'ID:(.*?)\|TS:(.*?)\|DATA:(.*)', line)
    if not match:
        print("INVALID_LINE")
        continue

    id_str, ts_str, data_str = match.groups()
    try:
        ts = int(ts_str)
    except ValueError:
        print("INVALID_LINE")
        continue

    print(f"{id_str.upper()},{ts + offset},{data_str[::-1]}")
EOF
    chmod +x /app/oracle_parser

    # Create the video with 37 black frames followed by 50 white frames at 24fps
    ffmpeg -f lavfi -i color=c=black:s=320x240:r=24 -vframes 37 -c:v libx264 /tmp/black.mp4
    ffmpeg -f lavfi -i color=c=white:s=320x240:r=24 -vframes 50 -c:v libx264 /tmp/white.mp4
    cat << 'EOF' > /tmp/inputs.txt
file '/tmp/black.mp4'
file '/tmp/white.mp4'
EOF
    ffmpeg -f concat -safe 0 -i /tmp/inputs.txt -c copy /app/dataset_recording.mp4
    rm -f /tmp/black.mp4 /tmp/white.mp4 /tmp/inputs.txt

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app