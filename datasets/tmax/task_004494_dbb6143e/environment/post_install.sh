apt-get update && apt-get install -y python3 python3-pip tesseract-ocr
pip3 install pytest numpy scipy flask fastapi uvicorn pillow pytesseract requests

mkdir -p /app
cat << 'EOF' > /tmp/gen_img.py
from PIL import Image, ImageDraw
img = Image.new('RGB', (800, 200), color = (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10,50), "Use mesh dimension N=40. Apply Tikhonov regularization lambda=0.005.", fill=(0,0,0))
img.save('/app/spec.png')
EOF
python3 /tmp/gen_img.py
rm /tmp/gen_img.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user