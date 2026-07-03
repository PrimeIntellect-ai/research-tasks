apt-get update && apt-get install -y python3 python3-pip espeak openssl gcc
    pip3 install pytest

    # Create directories
    mkdir -p /app/certs
    mkdir -p /app/.hidden

    # Generate audio file
    espeak -w /app/voicemail.wav "echo tango seven niner two"

    # Generate certificate chain
    cd /app/certs
    openssl genrsa -out root.key 2048
    openssl req -x509 -new -nodes -key root.key -sha256 -days 1024 -out root.crt -subj "/C=US/ST=State/L=City/O=Org/CN=RootCA"

    openssl genrsa -out intermediate.key 2048
    openssl req -new -key intermediate.key -out intermediate.csr -subj "/C=US/ST=State/L=City/O=Org/CN=IntermediateCA"
    cat <<EOF > v3_ext.cnf
[ v3_ca ]
basicConstraints = CA:TRUE
EOF
    openssl x509 -req -in intermediate.csr -CA root.crt -CAkey root.key -CAcreateserial -out intermediate.crt -days 500 -sha256 -extfile v3_ext.cnf -extensions v3_ca

    openssl genrsa -out leaf.key 2048
    openssl req -new -key leaf.key -out leaf.csr -subj "/C=US/ST=State/L=City/O=Org/CN=LeafCert"
    openssl x509 -req -in leaf.csr -CA intermediate.crt -CAkey intermediate.key -CAcreateserial -out leaf.crt -days 500 -sha256

    # Create encryptor.c
    cat <<'EOF' > /app/encryptor.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // LCG state initialized with (sum of ASCII of "et792") * 65537
    // "et792" = 101 + 116 + 55 + 57 + 50 = 379
    // 379 * 65537 = 24838523
    unsigned long long state = 379ULL * 65537ULL;
    int c;
    while ((c = getchar()) != EOF) {
        state = (state * 1103515245 + 12345) & 0x7fffffff;
        putchar(c ^ (state & 0xFF));
    }
    return 0;
}
EOF

    # Compile encryptor as reference_decryptor (since XOR is symmetric)
    gcc -o /app/.hidden/reference_decryptor /app/encryptor.c

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user