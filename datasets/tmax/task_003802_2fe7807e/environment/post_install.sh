apt-get update && apt-get install -y python3 python3-pip curl build-essential binutils xxd openssl cargo jq
    pip3 install pytest

    mkdir -p /home/user/forensics
    cd /home/user/forensics

    # 1. Create the C2 Key
    KEY_HEX="5f3a9b21c4e8d7f0a1b2c3d4e5f6a7b8"

    # 2. Create the malware source and compile it with the custom section
    cat << 'EOF' > malware_agent.c
#include <stdio.h>
int main() {
    printf("C2 Agent running...\n");
    return 0;
}
EOF

    # Create the binary payload for the key
    echo -n "$KEY_HEX" | xxd -r -p > key.bin

    # Compile the dummy malware
    gcc malware_agent.c -o malware_agent_tmp

    # Add the key to a custom section
    objcopy --add-section .c2_key=key.bin --set-section-flags .c2_key=alloc,readonly malware_agent_tmp malware_agent
    rm malware_agent.c malware_agent_tmp key.bin
    chmod +x malware_agent

    # 3. Generate a fake TLS certificate
    mkdir -p /tmp/certs
    openssl req -x509 -newkey rsa:2048 -keyout /tmp/certs/key.pem -out /tmp/certs/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Hacker/CN=c2.evil.com" 2>/dev/null

    # 4. Create the plaintext payload
    cat << 'EOF' > exfiltrated.dec
[INFO] C2 Agent started successfully.
[INFO] Target environment: Production Web Server
[CONFIG] Loaded C2 TLS Certificate for secure comms:
EOF
    cat /tmp/certs/cert.pem >> exfiltrated.dec
    cat << 'EOF' >> exfiltrated.dec
[INFO] Certificate loaded.
[LOG] Initial compromise vector logged below:
[INJECTION] username=admin' UNION SELECT password, salt FROM users WHERE is_admin=1--
[INFO] Exfiltration complete.
EOF

    # 5. Encrypt the payload using Python (repeating XOR)
    cat << 'EOF' > encrypt.py
import sys

def xor_crypt(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

with open('exfiltrated.dec', 'rb') as f:
    plaintext = f.read()

key = bytes.fromhex(sys.argv[1])
ciphertext = xor_crypt(plaintext, key)

with open('exfiltrated.enc', 'wb') as f:
    f.write(ciphertext)
EOF

    python3 encrypt.py "$KEY_HEX"
    rm encrypt.py exfiltrated.dec
    rm -rf /tmp/certs

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/forensics
    chmod -R 777 /home/user