apt-get update && apt-get install -y python3 python3-pip tesseract-ocr sqlite3 sqlcipher
    pip3 install pytest pillow

    mkdir -p /app/corpus/clean
    mkdir -p /app/corpus/evil

    # Create the user
    useradd -m -s /bin/bash user || true

    # Generate the admin token screenshot
    cat << 'EOF' > /tmp/gen_image.py
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (200, 50), color = (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10,10), "A7X9F2B4Q8M1V5C0", fill=(0,0,0))
img.save('/app/admin_token_screenshot.png')
EOF
    python3 /tmp/gen_image.py

    # Create dummy database and wal
    touch /app/telemetry_cache.db
    touch /app/telemetry_cache.db-wal

    # Create dummy core dump and log
    echo "dummy core dump" > /app/core.dump
    echo "dummy container log" > /app/container.log

    # Create telemetry parser
    cat << 'EOF' > /home/user/telemetry_parser.py
import json

def parse_telemetry(data):
    return json.loads(data)
EOF

    # Create corpus files
    echo '{"sensor": 1.23}' > /app/corpus/clean/1.json
    echo '{"sensor": NaN}' > /app/corpus/evil/1.json

    chmod -R 777 /home/user
    chmod -R 777 /app