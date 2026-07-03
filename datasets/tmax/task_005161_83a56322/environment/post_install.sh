apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest

# Install task dependencies
apt-get install -y ffmpeg python3-numpy python3-scipy gcc libc6-dev

# Create app directory
mkdir -p /app

# Generate carrier audio file
ffmpeg -f lavfi -i "sine=frequency=440:duration=5" -acodec pcm_s16le -ac 1 -ar 44100 /app/carrier.wav

# Create verification script
cat << 'EOF' > /app/verify_stego.py
import sys
import numpy as np
from scipy.io import wavfile

def decode_lsb(audio_data, max_len=50):
    bits = audio_data & 1
    chars = []
    for i in range(max_len):
        byte_bits = bits[i*8:(i+1)*8]
        if len(byte_bits) < 8:
            break
        val = sum([bit << j for j, bit in enumerate(byte_bits)])
        if val == 0:
            break
        chars.append(chr(val))
    return "".join(chars)

try:
    sr1, orig = wavfile.read('/app/carrier.wav')
    sr2, stego = wavfile.read('/home/user/payload.wav')

    if len(orig) != len(stego):
        print(0.0)
        sys.exit(0)

    token = decode_lsb(stego)
    if token != "AUTH_TOKEN_9942_EXFIL":
        print(0.0)
        sys.exit(0)

    orig_float = orig.astype(np.float64)
    stego_float = stego.astype(np.float64)
    mse = np.mean((orig_float - stego_float) ** 2)

    if mse == 0:
        psnr = 100.0
    else:
        max_pixel = 32767.0
        psnr = 10 * np.log10((max_pixel ** 2) / mse)

    print(f"{psnr:.2f}")

except Exception as e:
    print(0.0)
EOF

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user