apt-get update && apt-get install -y python3 python3-pip gcc libssl-dev
    pip3 install pytest

    mkdir -p /home/user/vuln_logger
    cat << 'EOF' > /home/user/vuln_logger/logger.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/md5.h>

#define SALT "H4rdc0d3dS4lt_991"
#define FLAG "FLAG{crYpt0_l0gg3r_byp4ss_772}"

void compute_md5(const char *str, char *output) {
    unsigned char digest[MD5_DIGEST_LENGTH];
    MD5_CTX ctx;
    MD5_Init(&ctx);
    MD5_Update(&ctx, str, strlen(str));
    MD5_Final(digest, &ctx);
    for (int i = 0; i < MD5_DIGEST_LENGTH; i++) {
        sprintf(&output[i*2], "%02x", (unsigned int)digest[i]);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <input_file> <audit_log>\n", argv[0]);
        return 1;
    }

    FILE *in = fopen(argv[1], "r");
    if (!in) {
        perror("Failed to open input file");
        return 1;
    }

    FILE *out = fopen(argv[2], "a");
    if (!out) {
        perror("Failed to open audit log");
        fclose(in);
        return 1;
    }

    char line[512];
    while (fgets(line, sizeof(line), in)) {
        line[strcspn(line, "\n")] = 0; // strip newline

        char token[32], checksum[64], message[256];
        if (sscanf(line, "%31[^:]:%63[^:]:%255[^\n]", token, checksum, message) == 3) {
            char to_hash[512];
            snprintf(to_hash, sizeof(to_hash), "%s%s%s", token, message, SALT);

            char expected_checksum[33];
            compute_md5(to_hash, expected_checksum);

            if (strcmp(checksum, expected_checksum) == 0) {
                if (strcmp(token, "ADMIN") == 0) {
                    fprintf(out, "[CORR_ID: 9812] [AUTH: ADMIN] [FLAG: %s] Message: %s\n", FLAG, message);
                } else {
                    fprintf(out, "[CORR_ID: %d] [AUTH: %s] Message: %s\n", rand() % 1000, token, message);
                }
            } else {
                fprintf(out, "INVALID_CHECKSUM for message: %s\n", message);
            }
        }
    }

    fclose(in);
    fclose(out);
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user