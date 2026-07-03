apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest flask pycryptodome requests

    mkdir -p /home/user/public
    echo "CTF{ab501ut3_p4th_j0in_ftw}" > /home/user/flag.txt

    cat << 'EOF' > /home/user/crypto_config.json
{
  "key": "Sixteen byte key",
  "iv": "Sixteen byte iv.",
  "pin_hash": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
}
EOF

    cat << 'EOF' > /home/user/app.py
from flask import Flask, request, send_file
import hashlib
from Crypto.Cipher import AES
import base64
import json
import os

app = Flask(__name__)

with open('/home/user/crypto_config.json') as f:
    config = json.load(f)
KEY = config['key'].encode()
IV = config['iv'].encode()
PIN_HASH = config['pin_hash']

def decrypt(data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted = cipher.decrypt(base64.b64decode(data))
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode()

@app.route('/download', methods=['POST'])
def download():
    pin = request.form.get('pin', '')
    if hashlib.sha256(pin.encode()).hexdigest() != PIN_HASH:
        return "Access denied", 403

    enc_filename = request.form.get('filename', '')
    try:
        filename = decrypt(enc_filename)
    except Exception:
        return "Decryption failed", 400

    # Simple WAF
    if '../' in filename:
        return "WAF blocked request", 403

    filepath = os.path.join('/home/user/public', filename)
    if not os.path.exists(filepath):
        return "File not found", 404

    return send_file(filepath)

if __name__ == '__main__':
    app.run(port=5000)
EOF

    chmod 644 /home/user/crypto_config.json /home/user/app.py /home/user/flag.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user