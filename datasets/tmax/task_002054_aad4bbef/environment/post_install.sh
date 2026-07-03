apt-get update && apt-get install -y python3 python3-pip tesseract-ocr
    pip3 install pytest Pillow

    mkdir -p /app

    cat << 'EOF' > /tmp/setup.py
import random
import string
from PIL import Image, ImageDraw

# Create Image
img = Image.new('RGB', (800, 200), color = (20, 20, 20))
d = ImageDraw.Draw(img)
text = "IDS ALERT: Credential leak in process arguments detected.\nTarget Prefix: SEC_AUTH_\nPayload: exactly 16 lowercase hex characters."
d.text((10,10), text, fill=(255,50,50))
img.save('/app/dashboard.png')

# Create logs
with open('/app/process_events.log', 'w') as f, open('/app/expected_events.log', 'w') as fe:
    for i in range(10000):
        # Generate some noise
        cmd = f"user{i%10} /bin/worker "
        if random.random() < 0.2:
            # Valid leaked token
            payload = ''.join(random.choices("0123456789abcdef", k=16))
            cmd += f"--token SEC_AUTH_{payload} --verbose"
            expected = cmd.replace(payload, "[REDACTED]")
        elif random.random() < 0.1:
            # Invalid length or uppercase (should NOT be redacted)
            payload = ''.join(random.choices("0123456789ABCDEF", k=12))
            cmd += f"--token SEC_AUTH_{payload}"
            expected = cmd
        else:
            cmd += "--status check"
            expected = cmd
        f.write(cmd + "\n")
        fe.write(expected + "\n")
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 755 /app