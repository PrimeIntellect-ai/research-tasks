apt-get update && apt-get install -y python3 python3-pip tesseract-ocr cron fonts-dejavu
    pip3 install pytest Pillow

    mkdir -p /app/corpora/evil /app/corpora/clean

    # Generate the config image using Python and Pillow
    cat << 'EOF' > /tmp/gen_image.py
from PIL import Image, ImageDraw, ImageFont

# Create a white image
img = Image.new('RGB', (1000, 200), color='white')
d = ImageDraw.Draw(img)

# Load a font
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
except IOError:
    font = ImageFont.load_default()

# Draw text
d.text((10, 50), r"CRON: */10 * * * *", fill='black', font=font)
d.text((10, 100), r"REGEX: ^[A-Za-z0-9 \u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]+$", fill='black', font=font)

# Save image
img.save('/app/config.png')
EOF

    python3 /tmp/gen_image.py
    rm /tmp/gen_image.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user