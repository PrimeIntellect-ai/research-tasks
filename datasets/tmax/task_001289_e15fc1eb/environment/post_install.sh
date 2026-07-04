apt-get update && apt-get install -y python3 python3-pip gcc libc6-dev
    pip3 install pytest

    mkdir -p /home/user/workspace
    cd /home/user/workspace

    # 1. Generate fake cert
    cat << 'EOF' > server_cert.pem
-----BEGIN CERTIFICATE-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy... [Truncated fake cert data]
TEST_CERTIFICATE_DATA_FOR_KEY_GENERATION
-----END CERTIFICATE-----
EOF

    # 2. Write auth_server.c
    cat << 'EOF' > auth_server.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void get_key(char *key_out) {
    // In a real scenario, this would compute the MD5 of the cert.
    // For simplicity in this self-contained mock, we use a static derived key.
    strcpy(key_out, "s3cr3tk3y");
}

void decrypt_payload(const char *hex_in, char *text_out) {
    char key[16];
    get_key(key);
    int key_len = strlen(key);
    int len = strlen(hex_in) / 2;
    for (int i = 0; i < len; i++) {
        unsigned int byte;
        sscanf(&hex_in[i * 2], "%02x", &byte);
        text_out[i] = byte ^ key[i % key_len];
    }
    text_out[len] = '\0';
}

int verify_sig(const char *payload, const char *sig) {
    if (strcmp(sig, "NONE") == 0) {
        return 1; // VULNERABLE: Bypass signature check
    }
    // Dummy check for other signatures
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <token>\n", argv[0]);
        return 1;
    }

    char *token = strdup(argv[1]);
    char *dot = strchr(token, '.');
    if (!dot) {
        printf("Invalid token format.\n");
        return 1;
    }

    *dot = '\0';
    char *hex_payload = token;
    char *signature = dot + 1;

    if (!verify_sig(hex_payload, signature)) {
        printf("Signature verification failed.\n");
        return 1;
    }

    char payload[256] = {0};
    decrypt_payload(hex_payload, payload);

    if (strstr(payload, "role=admin") != NULL && strstr(payload, "user=auditor") != NULL) {
        printf("FLAG{alg_n0n3_byp4ss_c_impl}\n");
    } else {
        printf("Access denied. User payload: %s\n", payload);
    }

    free(token);
    return 0;
}
EOF

    # 3. Compile the binary
    gcc auth_server.c -o auth_check

    # 4. Generate a valid log file
    cat << 'EOF' > requests.log
GET /dashboard HTTP/1.1
Host: internal.corp
Cookie: session_id=12345; auth_token=0400001711110a1b5d110f0e0c1b0c0a0c.VALID_SIG_8A9B
User-Agent: Mozilla/5.0
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/workspace
    chmod -R 777 /home/user