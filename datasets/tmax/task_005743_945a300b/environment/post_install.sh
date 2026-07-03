apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/evidence

    cat << 'EOF' > /home/user/evidence/capture.log
GET /api/login HTTP/1.1
Host: web.internal
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Cookie: theme=dark; session_token=abc123def456; password=supersecret
X-Timestamp: 1700000000

POST /api/upload HTTP/1.1
Host: web.internal
User-Agent: Mozilla/5.0 (X11; Linux x86_64) CustomClient/9.0
Cookie: session_token=hacker999; theme=light
X-Secret-Knock: open
X-Timestamp: 1700000042
EOF

    cat << 'EOF' > /home/user/evidence/verify_token.py
import hashlib

def generate_token(user_agent, timestamp):
    salt = "salty_backdoor_99"
    # Token is SHA256 of User-Agent + Timestamp + salt
    raw = user_agent.strip() + timestamp.strip() + salt
    return hashlib.sha256(raw.encode()).hexdigest()
EOF

    cat << 'EOF' > /home/user/evidence/decrypt.py
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=True)
    args = parser.parse_args()

    # Expected token based on the log's secret knock request:
    # User-Agent: Mozilla/5.0 (X11; Linux x86_64) CustomClient/9.0
    # Timestamp: 1700000042
    # Salt: salty_backdoor_99
    expected_token = "21e48bc8945cf40f92ab8d0df5c279d0ad185be669041a6b0c6df0473ce1ee42"

    if args.token == expected_token:
        with open('/home/user/evidence/recovered.txt', 'w') as f:
            f.write("CONFIDENTIAL_PROJECT_OMEGA_BLUEPRINTS_V1")
        print("Decryption successful. Recovered data written to recovered.txt")
    else:
        print("Invalid token. Decryption failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

    echo "U2FsdGVkX1+dummy_data_encrypted_payload..." > /home/user/evidence/stolen_data.enc

    chmod -R 777 /home/user