apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        openmpi-bin \
        libopenmpi-dev \
        tesseract-ocr \
        fonts-dejavu-core

    pip3 install --default-timeout=100 pytest numpy mpi4py pytesseract Pillow scipy

    mkdir -p /app

    cat << 'EOF' > /app/setup_data.py
import numpy as np
from PIL import Image, ImageDraw

# Generate raw spectra
np.random.seed(42)
U = np.random.randn(1000, 100, 12)
V = np.random.randn(1000, 12, 100)
signal = np.matmul(U, V)
noise = np.random.randn(1000, 100, 100) * 0.1
raw = signal + noise
np.save('/app/raw_spectra.npy', raw)

# Generate reference spectra
ref = np.zeros_like(raw)
for i in range(1000):
    u, s, vh = np.linalg.svd(raw[i], full_matrices=False)
    s[12:] = 0
    ref[i] = np.dot(u, np.dot(np.diag(s), vh))
np.save('/app/reference_spectra.npy', ref)

# Generate image
img = Image.new('RGB', (400, 100), color='white')
d = ImageDraw.Draw(img)
d.text((10, 50), "SVD_TRUNCATION_K=12", fill='black')
img.save('/app/config_memo.png')
EOF

    python3 /app/setup_data.py
    rm /app/setup_data.py

    cat << 'EOF' > /app/spectral_denoise.py
import numpy as np
import time

def main():
    start = time.time()
    raw = np.load('/app/raw_spectra.npy')

    # TODO: Extract k from /app/config_memo.png using OCR
    k = 1 

    # TODO: Parallelize with mpi4py
    out = np.zeros_like(raw)
    for i in range(len(raw)):
        u, s, vh = np.linalg.svd(raw[i], full_matrices=False)
        s[k:] = 0
        out[i] = np.dot(u, np.dot(np.diag(s), vh))

    np.save('/home/user/output_spectra.npy', out)
    end = time.time()

    with open('/home/user/timing.log', 'w') as f:
        f.write(str(end - start))

if __name__ == '__main__':
    main()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user