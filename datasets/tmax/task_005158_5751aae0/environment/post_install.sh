apt-get update && apt-get install -y python3 python3-pip tesseract-ocr g++ fonts-liberation
    pip3 install pytest Pillow

    mkdir -p /app

    # Generate the priors.png image
    python3 -c '
from PIL import Image, ImageDraw, ImageFont
img = Image.new("RGB", (600, 300), color="white")
d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 40)
except:
    font = ImageFont.load_default()
text = "Prior Mean: 0.0\nPrior Variance: 10.0\nSensor Variance: 2.5"
d.text((20, 20), text, fill="black", font=font)
img.save("/app/priors.png")
'

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app