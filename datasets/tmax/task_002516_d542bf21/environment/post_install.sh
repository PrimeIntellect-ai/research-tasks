apt-get update && apt-get install -y python3 python3-pip gcc make libssl-dev libseccomp-dev
    pip3 install pytest

    # Create app directory
    mkdir -p /app/secure_uploader_src

    # Create decoder.c
    cat << 'EOF' > /app/secure_uploader_src/decoder.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int decode_base64(const char *input, char **output) {
    int len = strlen(input);
    if (len % 4 == 0) len -= 1; // Vulnerability
    *output = strdup("decoded_payload");
    return 0;
}
EOF

    # Create handler.c
    cat << 'EOF' > /app/secure_uploader_src/handler.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int decode_base64(const char *input, char **output);
void setup_sandbox();

int main(int argc, char *argv[]) {
    if (argc != 4) return 1;
    char *payload = argv[1];
    char *filename = argv[2];
    char *cert = argv[3];

    // Missing path traversal check

    setup_sandbox();

    char *decoded;
    decode_base64(payload, &decoded);

    FILE *f = fopen(filename, "w");
    if (f) {
        fprintf(f, "%s", decoded);
        fclose(f);
    }
    free(decoded);
    return 0;
}
EOF

    # Create sandbox.c
    cat << 'EOF' > /app/secure_uploader_src/sandbox.c
#include <stdio.h>

void setup_sandbox() {
    // Dummy seccomp setup
}
EOF

    # Create Makefile
    cat << 'EOF' > /app/secure_uploader_src/Makefile
CC = gcc
CFLAGS = -Wall -g
LDFLAGS = 

all: secure_uploader

secure_uploader: handler.o decoder.o sandbox.o
	$(CC) $(CFLAGS) -o secure_uploader handler.o decoder.o sandbox.o $(LDFLAGS)

clean:
	rm -f *.o secure_uploader
EOF

    # Create oracle program
    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/oracle.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 4) return 1;
    char *payload = argv[1];
    char *filename = argv[2];
    char *cert = argv[3];

    if (strstr(filename, "..") || filename[0] == '/') return 2;

    char *decoded = strdup("decoded_payload");

    FILE *f = fopen(filename, "w");
    if (f) {
        fprintf(f, "%s", decoded);
        fclose(f);
    }
    free(decoded);
    return 0;
}
EOF
    gcc -o /opt/oracle/secure_uploader_oracle /opt/oracle/oracle.c
    chmod +x /opt/oracle/secure_uploader_oracle

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app/secure_uploader_src