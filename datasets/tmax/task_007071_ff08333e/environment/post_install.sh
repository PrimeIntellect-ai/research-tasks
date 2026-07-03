apt-get update && apt-get install -y python3 python3-pip git gcc make gdb
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/packet_decoder
    cd /home/user/packet_decoder

    git init
    git config user.email "oncall@example.com"
    git config user.name "OnCall Engineer"

    cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-g -O0 -Wall

packet_decoder: main.c decoder.c
	$(CC) $(CFLAGS) -o packet_decoder main.c decoder.c

clean:
	rm -f packet_decoder
EOF

    cat << 'EOF' > decoder.h
#ifndef DECODER_H
#define DECODER_H
void decode_packet(const char* input, int len, char* output);
#endif
EOF

    cat << 'EOF' > decoder.c
#include "decoder.h"
#include <stdio.h>

void decode_packet(const char* input, int len, char* output) {
    for (int i = 0; i < len; i++) {
        output[i] = input[i] ^ 0x42;
    }
    output[len] = '\0';
}
EOF

    cat << 'EOF' > main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "decoder.h"

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: %s <file>\n", argv[0]);
        return 1;
    }

    FILE* f = fopen(argv[1], "rb");
    if (!f) return 1;

    char buffer[256];
    char decoded[256];

    while (fread(buffer, 1, 16, f) == 16) {
        decode_packet(buffer, 16, decoded);
        printf("%s\n", decoded);
    }

    fclose(f);
    return 0;
}
EOF

    git add Makefile main.c decoder.h decoder.c
    git commit -m "Initial working commit"
    git tag v1.0

    sed -i 's/char buffer\[256\]/char buffer\[512\]/g' main.c
    git commit -am "Increase buffer size"

    sed -i 's/char decoded\[256\]/char decoded\[512\]/g' main.c
    git commit -am "Increase decode buffer size"

    cat << 'EOF' > decoder.c
#include "decoder.h"
#include <stdio.h>

void decode_packet(const char* input, int len, char* output) {
    // Optimized loop condition
    for (int i = 0; i <= len; i++) {
        output[i] = input[i] ^ 0x42;
    }
    output[len] = '\0';
}
EOF
    git commit -am "Optimize loop conditions in decoder"
    BAD_COMMIT=$(git rev-parse HEAD)

    sed -i 's/-O0/-O2/g' Makefile
    git commit -am "Optimize Makefile flags"

    echo "// End of file" >> main.c
    git commit -am "Add comment to main"

    cd /home/user
    python3 -c "
with open('prod_dump.dat', 'wb') as f:
    messages = [b'SYSTEM_START_OK_', b'USER_AUTH_SUCCES', b'DB_CONNECT_READY']
    for m in messages:
        encoded = bytes([b ^ 0x42 for b in m])
        f.write(encoded)
"

    echo "$BAD_COMMIT" > /tmp/.hidden_bad_commit

    chown -R user:user /home/user/packet_decoder
    chown user:user /home/user/prod_dump.dat

    chmod -R 777 /home/user