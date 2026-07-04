apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ffmpeg \
        tesseract-ocr \
        tesseract-ocr-eng \
        fonts-liberation

    pip3 install pytest Pillow

    mkdir -p /app

    cat << 'EOF' > /tmp/gen.py
import os, json, hashlib, base64, subprocess
from PIL import Image, ImageDraw, ImageFont

cert = """-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAJC1HiIAZAiIMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMTkwNzI0MTcyNDEyWhcNMjkwNzIxMTcyNDEyWjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAuK5
-----END CERTIFICATE-----
"""
sha256 = hashlib.sha256(cert.encode()).hexdigest()
data = {
    "cert_b64": base64.b64encode(cert.encode()).decode(),
    "expected_cookie": "c2_session=v9x8b7a6m5n4",
    "sha256_checksum": sha256
}
b64_json = base64.b64encode(json.dumps(data).encode()).decode()

chunk = len(b64_json) // 10
parts = [b64_json[i*chunk:(i+1)*chunk] for i in range(9)]
parts.append(b64_json[9*chunk:])

os.makedirs("/tmp/frames", exist_ok=True)
font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 40)

for i in range(300):
    img = Image.new('RGB', (1280, 720), color='white')
    if i % 30 == 0 and (i // 30) < 10:
        draw = ImageDraw.Draw(img)
        draw.text((50, 300), parts[i // 30], fill='black', font=font)
    img.save(f"/tmp/frames/frame_{i:03d}.png")

subprocess.run([
    "ffmpeg", "-y", "-framerate", "30", 
    "-i", "/tmp/frames/frame_%03d.png", 
    "-c:v", "libx264", "-pix_fmt", "yuv420p", 
    "/app/exfiltration_feed.mp4"
], check=True)
EOF

    python3 /tmp/gen.py
    rm -rf /tmp/frames /tmp/gen.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app