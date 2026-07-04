apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Create the policy image
    convert -size 1000x200 xc:white -font DejaVu-Sans -pointsize 24 -fill black -draw "text 20,100 'CONFIDENTIAL POLICY - XOR_KEY=0x3F, REQUIRED_COOKIE_PREFIX=ComplianceSessionID'" /app/policy_rules.png

    # Create the oracle extractor
    cat << 'EOF' > /app/oracle_extractor
#!/usr/bin/env python3
import sys
import base64
import re

def main():
    if len(sys.argv) < 2:
        print("AUDIT_ERROR: Invalid payload")
        return
    try:
        decoded = base64.b64decode(sys.argv[1])
        decrypted = bytes([b ^ 0x3F for b in decoded]).decode('utf-8', errors='ignore')

        hash_match = re.search(r'X-ELF-Hash:\s*([a-f0-9]{64})', decrypted)
        cookie_match = re.search(r'Cookie:.*?ComplianceSessionID=([a-zA-Z0-9]+)', decrypted)

        if hash_match and cookie_match:
            print(f"AUDIT_EVENT: Hash={hash_match.group(1)} Cookie={cookie_match.group(1)}")
        else:
            print("AUDIT_ERROR: Invalid payload")
    except Exception:
        print("AUDIT_ERROR: Invalid payload")

if __name__ == "__main__":
    main()
EOF
    chmod +x /app/oracle_extractor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user