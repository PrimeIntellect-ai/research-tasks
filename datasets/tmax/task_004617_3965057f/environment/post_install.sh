apt-get update && apt-get install -y python3 python3-pip gcc rustc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create dummy secret.enc
    echo "encrypted data" > /home/user/secret.enc

    # Create the mock vuln_auth binary
    cat << 'EOF' > /tmp/vuln_auth.c
#include <stdio.h>
#include <string.h>

const char *service_id = "SVC_b3a8e9f1";

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <token>\n", argv[0]);
        return 1;
    }

    const char *expected = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJyb2xlIjoiYWRtaW4iLCJzZXJ2aWNlX2lkIjoiU1ZDX2IzYThlOWYxIn0.";

    if (strcmp(argv[1], expected) == 0) {
        FILE *f = fopen("/home/user/flag.txt", "w");
        if (f) {
            fprintf(f, "FLAG{rust_jwt_alg_none_exploited_992}");
            fclose(f);
            printf("Decrypted secret.enc successfully.\n");
        }
    } else {
        printf("Invalid token.\n");
    }
    return 0;
}
EOF
    gcc /tmp/vuln_auth.c -o /home/user/vuln_auth
    rm /tmp/vuln_auth.c

    chmod -R 777 /home/user