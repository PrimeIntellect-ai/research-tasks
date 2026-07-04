apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install dependencies for compilation, audio generation, and binary analysis
    apt-get install -y gcc libssl-dev espeak binutils strace ltrace gdb

    mkdir -p /app

    # Generate the audio file
    espeak -w /app/salt_dictation.wav "The new salt is secure_rotate_99"

    # Write the C source for the verifiers
    cat << 'EOF' > /tmp/verifier.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>

void replace_all(char *str, const char *sub) {
    char *pos;
    int len = strlen(sub);
    while ((pos = strstr(str, sub)) != NULL) {
        memmove(pos, pos + len, strlen(pos + len) + 1);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    char *input = strdup(argv[1]);

    replace_all(input, "' OR '1'='1");
    replace_all(input, "<script>");

    int buf_len = strlen(input) + strlen(SALT) + 1;
    char *buffer = malloc(buf_len);
    snprintf(buffer, buf_len, "%s%s", input, SALT);

    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char*)buffer, strlen(buffer), hash);

    for(int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");

    free(input);
    free(buffer);
    return 0;
}
EOF

    # Compile the legacy oracle verifier (stripped)
    gcc -O2 -DSALT=\"legacy_salt_123\" -o /app/oracle_verifier /tmp/verifier.c -lssl -lcrypto -s

    # Compile the reference new salt verifier (stripped)
    gcc -O2 -DSALT=\"secure_rotate_99\" -o /app/oracle_verifier_new_salt /tmp/verifier.c -lssl -lcrypto -s

    # Cleanup
    rm /tmp/verifier.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user