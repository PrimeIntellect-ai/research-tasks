apt-get update && apt-get install -y python3 python3-pip tesseract-ocr
    pip3 install pytest Pillow pandas scikit-learn numpy pytesseract

    cat << 'EOF' > /tmp/setup.py
import os
import csv
import random
from PIL import Image, ImageDraw, ImageFont

os.makedirs('/app', exist_ok=True)

# 1. Create the Image Artifact with the Transformation Matrix
matrix_text = "M11: 0.8  M12: -0.6\nM21: 0.6  M22: 0.8"
img = Image.new('RGB', (400, 200), color=(255, 255, 255))
draw = ImageDraw.Draw(img)
draw.text((20, 50), "TRANSFORMATION MATRIX\n\n" + matrix_text, fill=(0,0,0))
img.save('/app/transformation.png')

# 2. Generate Dataset
random.seed(42)
weights = [3.5, -2.1] # True weights for Z1, Z2
bias = 10.0

def generate_data(n_samples, filename, include_y=True, inject_noise=True):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        if include_y:
            writer.writerow(['id', 'X1', 'X2', 'Y'])
        else:
            writer.writerow(['id', 'X1', 'X2'])

        y_true = {}
        for i in range(1, n_samples + 1):
            # Generate Z first
            z1 = random.uniform(-100, 100)
            z2 = random.uniform(-100, 100)

            # Inverse transform to get X1, X2
            x1 = 0.8 * z1 + 0.6 * z2
            x2 = -0.6 * z1 + 0.8 * z2

            y = bias + weights[0] * z1 + weights[1] * z2
            y_true[i] = y
            if inject_noise:
                y += random.gauss(0, 0.5)

            # Inject schema errors in training data
            if include_y and i % 20 == 0:
                x1 = "" # Missing value

            if include_y:
                writer.writerow([i, x1, x2, y])
            else:
                writer.writerow([i, x1, x2])
        return y_true

# Train data with noise and schema errors
generate_data(500, '/app/raw_data.csv', include_y=True)

# Test data without Y
test_true_y = generate_data(100, '/app/test_data.csv', include_y=False, inject_noise=False)

# Save true Y for the verifier
with open('/app/test_truth.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'Y_true'])
    for k, v in test_true_y.items():
        writer.writerow([k, v])

# Write verifier script
verifier_code = """import sys
import pandas as pd

try:
    pred_df = pd.read_csv('/home/user/predictions.csv')
    true_df = pd.read_csv('/app/test_truth.csv')
    merged = pd.merge(true_df, pred_df, on='id')
    mse = ((merged['Y_true'] - merged['Y_pred']) ** 2).mean()
    print(f"MSE: {mse}")
    if mse <= 2.0:
        sys.exit(0)
    else:
        sys.exit(1)
except Exception as e:
    print(f"Verification failed: {e}")
    sys.exit(1)
"""
with open('/app/verify.py', 'w') as f:
    f.write(verifier_code)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user