apt-get update && apt-get install -y python3 python3-pip openssl imagemagick tesseract-ocr tcpdump curl tshark
    pip3 install pytest scapy

    mkdir -p /app

    # 1. Create passphrase image
    # Fix imagemagick policy to allow writing
    sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/g' /etc/ImageMagick-6/policy.xml || true
    convert -size 400x100 xc:white -font DejaVu-Sans -pointsize 32 -fill black -draw "text 20,60 'S3cr3t_N3tw0rk_K3y'" /app/passphrase.png

    # 2. Generate RSA key and encrypt
    openssl genrsa -aes256 -passout pass:S3cr3t_N3tw0rk_K3y -out /app/server.key.enc 2048
    openssl rsa -in /app/server.key.enc -passin pass:S3cr3t_N3tw0rk_K3y -out /tmp/server.key
    openssl req -new -x509 -key /tmp/server.key -out /tmp/server.crt -days 365 -subj "/CN=localhost"

    # 3. Create HTML payload
    cat << 'EOF' > /tmp/payload.html
HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<!DOCTYPE html>
<html>
<head>
    <script src="https://trusted-cdn.example.com/app.js"></script>
    <link rel="stylesheet" href="https://internal-styles.example.com/main.css">
</head>
<body>
    <img src="https://trusted-images.example.com/logo.png">
    <script src="https://evil-crypto-miner.hacker.net/pwn.js"></script>
</body>
</html>
EOF

    # 4. Create PCAP
    # Start OpenSSL s_server using an older cipher suite that allows decryption with RSA key
    openssl s_server -key /tmp/server.key -cert /tmp/server.crt -accept 4443 -cipher TLS_RSA_WITH_AES_128_CBC_SHA -nocert -HTTP &
    SERVER_PID=$!
    sleep 2

    # Capture traffic
    tcpdump -i lo -w /app/traffic.pcap port 4443 &
    TCPDUMP_PID=$!
    sleep 2

    # Make request
    curl -k --cipher rsa_aes_128_cbc_sha_256 https://127.0.0.1:4443/tmp/payload.html || true
    sleep 2

    kill $TCPDUMP_PID || true
    kill $SERVER_PID || true
    sleep 1

    # Fallback if tcpdump failed to create the file
    if [ ! -f /app/traffic.pcap ]; then
        touch /app/traffic.pcap
    fi

    # 5. Create evaluator script
    cat << 'EOF' > /app/evaluate_csp.py
#!/usr/bin/env python3
import sys

if len(sys.argv) < 2:
    print("Score: 0")
    sys.exit(1)

csp = sys.argv[1].lower()
score = 100

if "default-src 'self'" not in csp:
    score -= 20

if "script-src" in csp:
    if "https://trusted-cdn.example.com" not in csp:
        score -= 30
    if "evil-crypto-miner" in csp or "*" in csp.split("script-src")[1].split(";")[0]:
        score -= 50
else:
    score -= 40

if "img-src" in csp:
    if "https://trusted-images.example.com" not in csp:
        score -= 15
else:
    score -= 10

if "style-src" in csp:
    if "https://internal-styles.example.com" not in csp:
        score -= 15
else:
    score -= 10

score = max(0, score)
print(f"Score: {score}")

if score >= 90:
    sys.exit(0)
else:
    sys.exit(1)
EOF
    chmod +x /app/evaluate_csp.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user