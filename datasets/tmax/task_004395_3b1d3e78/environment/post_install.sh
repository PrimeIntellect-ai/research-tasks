apt-get update && apt-get install -y python3 python3-pip golang tesseract-ocr
pip3 install pytest Pillow pytesseract

mkdir -p /app
cat << 'EOF' > /tmp/make_image.py
from PIL import Image, ImageDraw
img = Image.new('RGB', (400, 100), color = (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10,10), "ALPHA=0.25 BETA=0.10 GAMMA=0.05", fill=(0,0,0))
img.save('/app/reaction_rates.png')
EOF
python3 /tmp/make_image.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user