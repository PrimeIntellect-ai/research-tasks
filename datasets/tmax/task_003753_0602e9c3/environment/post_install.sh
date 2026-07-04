apt-get update && apt-get install -y python3 python3-pip openssh-client
pip3 install pytest cryptography

mkdir -p /home/user

# Create password file
cat << 'EOF' > /home/user/password.txt
S3cr3tP@ssw0rd!
EOF

# Create key_gen.py
cat << 'EOF' > /home/user/key_gen.py
import hashlib
import random

def get_key_and_iv(password):
    # Derive key
    key = hashlib.sha256(password.encode('utf-8')).digest()

    # Generate IV
    # Security note: using standard random for IV generation
    random.seed(1337)
    iv = bytes([random.randint(0, 255) for _ in range(16)])

    return key, iv
EOF

# Generate SSH keys and manifest
mkdir -p /home/user/vault_temp
ssh-keygen -t rsa -b 2048 -f /home/user/vault_temp/admin_key.pem -N "" -q
ssh-keygen -t rsa -b 2048 -f /home/user/vault_temp/backup_key.pem -N "" -q

cd /home/user/vault_temp
sha256sum admin_key.pem > /home/user/manifest.sha256
sha256sum backup_key.pem >> /home/user/manifest.sha256

# Corrupt backup_key.pem
echo "CORRUPTED DATA" >> /home/user/vault_temp/backup_key.pem

# Create tarball
tar -cf /home/user/vault_temp.tar admin_key.pem backup_key.pem
cd /home/user/

# Encrypt tarball
cat << 'EOF' > /home/user/encrypt_vault.py
import hashlib
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

password = "S3cr3tP@ssw0rd!"
key = hashlib.sha256(password.encode('utf-8')).digest()
random.seed(1337)
iv = bytes([random.randint(0, 255) for _ in range(16)])

with open('/home/user/vault_temp.tar', 'rb') as f:
    data = f.read()

padder = padding.PKCS7(128).padder()
padded_data = padder.update(data) + padder.finalize()

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

with open('/home/user/vault.enc', 'wb') as f:
    f.write(encrypted_data)
EOF

python3 /home/user/encrypt_vault.py

# Cleanup
rm -rf /home/user/vault_temp /home/user/vault_temp.tar /home/user/encrypt_vault.py

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user