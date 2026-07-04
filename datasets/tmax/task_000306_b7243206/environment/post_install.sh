apt-get update && apt-get install -y python3 python3-pip espeak zip openssl
    pip3 install pytest pyjwt cryptography pyinstaller

    mkdir -p /app
    cd /app

    # Create wordlist
    cat << 'EOF' > wordlist.txt
password
admin
qwerty
sunshine
hello
world
computer
security
EOF

    # Generate voicemail
    espeak -w voicemail.wav "Hello. To decrypt the bundle dot zip file, use a word from the provided wordlist dot txt, and append the number forty two to it."

    # Generate keys
    openssl genrsa -out private_key.pem 2048
    openssl rsa -in private_key.pem -pubout -out public_key.pem

    # Create spec.txt
    cat << 'EOF' > spec.txt
JWT Redactor Specification
--------------------------
Write an executable script at /home/user/jwt_processor that reads a single JWT string from standard input.
1. Parse the JWT.
2. If the header specifies 'alg': 'none' (case-insensitive), output "ERROR: Insecure algorithm" to stdout and exit 1.
3. Verify the JWT signature using the RSA public key in public_key.pem. If the signature is invalid or missing, output "ERROR: Invalid signature" to stdout and exit 2.
4. If valid, parse the JSON payload. If the keys 'email' or 'phone' exist at the top level, replace their string values with the exact string "[REDACTED]".
5. Output the resulting JSON payload to stdout, strictly minified (no spaces between keys/values), and exit 0.
EOF

    # Create bundle.zip
    zip --password sunshine42 bundle.zip spec.txt public_key.pem
    rm spec.txt

    # Create oracle script
    cat << 'EOF' > oracle.py
import sys
import json
import jwt

def main():
    token = sys.stdin.read().strip()
    if not token:
        sys.exit(2)

    try:
        unverified_header = jwt.get_unverified_header(token)
        if unverified_header.get('alg', '').lower() == 'none':
            print("ERROR: Insecure algorithm")
            sys.exit(1)
    except Exception:
        print("ERROR: Invalid signature")
        sys.exit(2)

    try:
        with open('/app/public_key.pem', 'rb') as f:
            public_key = f.read()

        decoded = jwt.decode(token, public_key, algorithms=['RS256'])
    except Exception:
        print("ERROR: Invalid signature")
        sys.exit(2)

    if 'email' in decoded:
        decoded['email'] = '[REDACTED]'
    if 'phone' in decoded:
        decoded['phone'] = '[REDACTED]'

    print(json.dumps(decoded, separators=(',', ':')))
    sys.exit(0)

if __name__ == '__main__':
    main()
EOF

    pyinstaller --onefile oracle.py
    mv dist/oracle /app/oracle_bin
    rm -rf build dist oracle.py oracle.spec

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user