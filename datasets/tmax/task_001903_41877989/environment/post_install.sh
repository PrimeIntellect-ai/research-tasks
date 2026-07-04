apt-get update && apt-get install -y python3 python3-pip espeak
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /app/oracle_redactor
#!/usr/bin/env python3
import sys
import re

def xor_crypt(data: bytes, key: bytes) -> bytes:
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def main():
    raw_req = sys.stdin.read()
    key = b"OMEGA99"

    def replacer(match):
        hex_val = match.group(1)
        try:
            decrypted = xor_crypt(bytes.fromhex(hex_val), key).decode('utf-8')
            redacted = re.sub(r'SSN=\d{9}', 'SSN=REDACTED', decrypted)
            reencrypted = xor_crypt(redacted.encode('utf-8'), key).hex().upper()
            return f"AuthToken={reencrypted}"
        except Exception:
            return match.group(0)

    # Replace AuthToken value using regex
    modified_req = re.sub(r'AuthToken=([0-9a-fA-F]+)', replacer, raw_req)
    sys.stdout.write(modified_req)

if __name__ == "__main__":
    main()
EOF
    chmod +x /app/oracle_redactor

    espeak -w /app/intercepted.wav "Attention network engineer. The open redirect vulnerability is patched, but we need you to redact sensitive traffic. The AuthToken cookie is encrypted using a repeating XOR cipher with the key OMEGA99. Find all nine digit Social Security Numbers prefixed by SSN equals, and replace the digits with the word REDACTED."

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user