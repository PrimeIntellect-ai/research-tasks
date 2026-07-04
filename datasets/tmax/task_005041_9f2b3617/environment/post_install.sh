apt-get update && apt-get install -y python3 python3-pip tesseract-ocr fonts-liberation
    pip3 install pytest pandas numpy pillow pyarrow fastparquet flask fastapi uvicorn requests pytesseract

    mkdir -p /app
    mkdir -p /home/user

    cat << 'EOF' > /tmp/setup.py
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

# Create Image
os.makedirs('/app', exist_ok=True)
img = Image.new('RGB', (400, 150), color=(255, 255, 255))
d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 24)
except:
    font = ImageFont.load_default()

d.text((10, 10), "Correlation_Threshold=0.85", fill=(0, 0, 0), font=font)
d.text((10, 60), "Token=sigma_clean_2024", fill=(0, 0, 0), font=font)
img.save('/app/cleaning_instructions.png')

# Create Dataset
np.random.seed(42)
n_samples = 1000
sensor_A = np.random.normal(0, 1, n_samples)
sensor_B = np.random.normal(0, 2, n_samples)
sensor_C = sensor_A * 0.95 + np.random.normal(0, 0.1, n_samples) # Correlated with A > 0.85
sensor_D = np.random.normal(0, 1.5, n_samples)
sensor_E = sensor_B * -0.90 + np.random.normal(0, 0.2, n_samples) # Correlated with B > 0.85

df = pd.DataFrame({
    'sensor_A': sensor_A,
    'sensor_B': sensor_B,
    'sensor_C': sensor_C,
    'sensor_D': sensor_D,
    'sensor_E': sensor_E
})
df.to_csv('/home/user/sensor_data.csv', index=False)
EOF

    python3 /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app