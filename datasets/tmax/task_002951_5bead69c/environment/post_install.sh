apt-get update && apt-get install -y python3 python3-pip tesseract-ocr
    pip3 install pytest Pillow

    mkdir -p /app /home/user

    # Generate the image
    python3 -c "
from PIL import Image, ImageDraw
img = Image.new('RGB', (400, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = 'ABI to CFLAGS Matrix:\nGLIBC_2.25 : -D_OLD_ABI -O1\nGLIBC_2.28 : -D_MID_ABI -O2\nGLIBC_2.34 : -D_NEW_ABI -O3 -shared'
d.text((10,10), text, fill=(0,0,0))
img.save('/app/abi_matrix.png')
"

    # Create the oracle
    cat << 'EOF' > /app/oracle_flags
#!/usr/bin/env python3
import sys

mapping = {
    "GLIBC_2.25": "-D_OLD_ABI -O1",
    "GLIBC_2.28": "-D_MID_ABI -O2",
    "GLIBC_2.34": "-D_NEW_ABI -O3 -shared"
}

for line in sys.stdin:
    line = line.strip('\n')
    flags = mapping.get(line, "UNKNOWN")
    print(f"TARGET {line}: {flags}")
EOF
    chmod +x /app/oracle_flags

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user