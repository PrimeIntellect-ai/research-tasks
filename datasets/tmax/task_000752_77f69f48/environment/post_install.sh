apt-get update && apt-get install -y python3 python3-pip tesseract-ocr
    pip3 install pytest pillow pytesseract

    mkdir -p /app
    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import struct
from PIL import Image, ImageDraw

# Create image
img = Image.new('RGB', (400, 200), color='white')
d = ImageDraw.Draw(img)
text = "SERVER CONFIGURATION\nAPI_PORT: 8134\nAUTH_TOKEN: sec_bkup_992a1"
d.text((10,10), text, fill='black')
img.save('/app/admin_notes.png')

# Create binary file
entries = [
    (b"config.txt", b"system=ready"),
    (b"../../../etc/shadow", b"root:x:0:0:root:/root:/bin/bash"),
    (b"/var/log/syslog", b"kernel panic"),
    (b"logs/server.log.part1", b"Line 1\nLine 2\n"),
    (b"logs/server.log.part2", b"Line 3\nLine 4\n"),
]

with open('/home/user/legacy_backup.bin', 'wb') as f:
    f.write(b"BKUP")
    for path, data in entries:
        f.write(struct.pack('<H', len(path)))
        f.write(path)
        f.write(struct.pack('<I', len(data)))
        f.write(data)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /app
    chmod -R 777 /home/user