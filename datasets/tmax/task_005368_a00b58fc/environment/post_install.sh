apt-get update && apt-get install -y python3 python3-pip gcc g++ make gdb strace binutils libssl-dev nlohmann-json3-dev
    pip3 install pytest cryptography

    mkdir -p /app
    cat << 'EOF' > /app/token_processor.c
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
    char key[] = "1234567890abcdef";
    char iv[16] = {0};
    char hmac_key[] = "secret_hmac_key_99";

    if (argc > 1 && strcmp(argv[1], "alg=none") == 0) {
        printf("Bypassing HMAC check\n");
    } else {
        printf("Checking HMAC with key: %s\n", hmac_key);
    }
    printf("Decrypting with key: %s\n", key);
    return 0;
}
EOF
    gcc -O2 /app/token_processor.c -o /app/token_processor
    strip /app/token_processor
    rm /app/token_processor.c

    useradd -m -s /bin/bash user || true

    # Generate some dummy logs
    cat << 'EOF' > /home/user/incident_logs.txt
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.U29tZSBlbmNyeXB0ZWQgcGF5bG9hZA==.U2lnbmF0dXJl
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0=.QW5vdGhlciBlbmNyeXB0ZWQgcGF5bG9hZA==.
EOF

    chmod -R 777 /home/user