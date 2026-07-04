apt-get update && apt-get install -y python3 python3-pip gcc make tesseract-ocr
    pip3 install pytest pillow

    mkdir -p /app
    cd /app

    cat << 'EOF' > generate_image.py
from PIL import Image, ImageDraw, ImageFont
import sys

text = "ALGORITHM: For each byte B in input, compute X = (B * 13 + 7) mod 256.\nIf X mod 2 == 0, Y = X / 2, else Y = X. Output Y as two-character hex."
img = Image.new('RGB', (800, 100), color = (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10,10), text, fill=(0,0,0))
img.save('/app/legacy_api_formula.png')
EOF
    python3 generate_image.py

    cat << 'EOF' > /app/oracle.c
#include <stdio.h>

int main() {
    int b;
    while ((b = fgetc(stdin)) != EOF) {
        int x = (b * 13 + 7) % 256;
        int y = (x % 2 == 0) ? (x / 2) : x;
        printf("%02x", y);
    }
    return 0;
}
EOF
    gcc -O3 /app/oracle.c -o /app/oracle_payload_transform
    chmod +x /app/oracle_payload_transform

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app