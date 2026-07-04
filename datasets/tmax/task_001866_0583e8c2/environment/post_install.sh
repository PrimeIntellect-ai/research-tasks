apt-get update && apt-get install -y python3 python3-pip ffmpeg git
    pip3 install pytest Pillow

    mkdir -p /app

    # Generate Video
    cat << 'EOF' > /tmp/gen_video.py
import os
from PIL import Image, ImageDraw

os.makedirs("/tmp/frames", exist_ok=True)
for i in range(1, 301):
    img = Image.new('RGB', (640, 480), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    text = "HEALTHY" if i < 214 else "CRITICAL"
    d.text((100, 200), text, fill=(255, 255, 255))
    img.save(f"/tmp/frames/frame_{i:03d}.png")
EOF
    python3 /tmp/gen_video.py
    ffmpeg -framerate 30 -i /tmp/frames/frame_%03d.png -c:v libx264 -pix_fmt yuv420p /app/dashboard.mp4
    rm -rf /tmp/frames /tmp/gen_video.py

    # Create Oracle Parser
    cat << 'EOF' > /app/oracle_parser
#!/usr/bin/env python3
import sys, json
line = sys.stdin.read().strip()
parts = line.split()
if len(parts) == 4:
    print(json.dumps({"timestamp": parts[0], "ip": parts[1], "action": parts[2], "status": parts[3]}))
else:
    print(json.dumps({"error": "malformed"}))
EOF
    chmod +x /app/oracle_parser

    # Create user and repo
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/uptime_repo
    cd /home/user/uptime_repo
    git init
    git config --global user.email "sre@company.com"
    git config --global user.name "SRE"

    cat << 'EOF' > parser.py
#!/usr/bin/env python3
import sys, json
line = sys.stdin.read().strip()
parts = line.split()
print(json.dumps({"timestamp": parts[0], "ip": parts[1], "action": parts[2], "status": parts[3]}))
EOF
    chmod +x parser.py
    git add parser.py
    git commit -m "Initial commit of parser"

    git rm parser.py
    git commit -m "Accidentally delete parser"

    chmod -R 777 /home/user