apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user

    # Create dummy video file
    touch /app/intercepted_session.mp4

    # Create reference sanitizer
    cat << 'EOF' > /app/reference_sanitizer.py
import sys
import os
import html

def sanitize(payload):
    # Simplified reference implementation
    normalized = os.path.normpath("/sandbox/" + payload)
    if not normalized.startswith("/sandbox/"):
        normalized = "/sandbox/"
    escaped = html.escape(normalized)
    return escaped

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(sanitize(sys.argv[1]))
EOF
    chmod 755 /app/reference_sanitizer.py

    # Create weak cipher implementation
    cat << 'EOF' > /home/user/weak_cipher.py
# Weak SPN Cipher Implementation
def encrypt(plaintext, key):
    pass # implementation omitted for setup

def decrypt(ciphertext, key):
    pass # implementation omitted for setup
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user