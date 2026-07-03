apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/.ssh

cat << 'EOF' > /home/user/legacy_auth.py
import sys

# Encrypted deployment key
ENCRYPTED_KEY_HEX = "0f050b0c160a000e00072b1d1f030d08221c051f3b392e212f3805141e1b1228221c051f2b050d04081c010a3b2b485901121d0a0b1c0b05130b1c05192b152e394859485948594859485948594859485948484848485901121d0a0b1c0b05130b1c05192b152e394859485948594859485948594859485948484848485901121d0a0b1c0b05130b1c05192b152e39485948594859485948594859485948"

def decrypt_key(pin: int) -> str:
    """
    Decrypts the SSH key using the provided 4-digit PIN.
    """
    pin_str = f"{pin:04d}"
    encrypted_bytes = bytes.fromhex(ENCRYPTED_KEY_HEX)
    decrypted = bytearray()

    for i, b in enumerate(encrypted_bytes):
        # Custom XOR cipher
        decrypted.append(b ^ ord(pin_str[i % 4]))

    return decrypted.decode('utf-8', errors='ignore')
EOF

chmod -R 777 /home/user
chmod 700 /home/user/.ssh
chown -R user:user /home/user