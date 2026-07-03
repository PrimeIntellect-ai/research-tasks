apt-get update && apt-get install -y python3 python3-pip gcc make gawk
    pip3 install pytest

    mkdir -p /app/libmalcrypt-0.5
    cd /app/libmalcrypt-0.5

    cat << 'EOF' > cipher.h
#ifndef CIPHER_H
#define CIPHER_H
#include <stdint.h>
void encrypt_block(uint32_t v[2], const uint32_t k[4]);
void decrypt_block(uint32_t v[2], const uint32_t k[4]);
#endif
EOF

    cat << 'EOF' > cipher.c
#include "cipher.h"
void encrypt_block(uint32_t v[2], const uint32_t k[4]) {
    uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;
    for (int i=0; i<4; i++) {
        sum += delta;
        v0 += ((v1<<4) + k[0]) ^ (v1 + sum) ^ ((v1>>5) + k[1]);
        v1 += ((v0<<4) + k[2]) ^ (v0 + sum) ^ ((v0>>5) + k[3]);
    }
    v[0]=v0; v[1]=v1;
}
void decrypt_block(uint32_t v[2], const uint32_t k[4]) {
    uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*4;
    for (int i=0; i<4; i++) {
        v1 -= ((v0<<4) + k[2]) ^ (v0 + sum) ^ ((v0>>5) + k[3]);
        v0 -= ((v1<<4) + k[0]) ^ (v1 + sum) ^ ((v1>>5) + k[1]);
        sum -= delta;
    }
    v[0]=v0; v[1]=v1;
}
EOF

    # Create Makefile avoiding % at the start of the line
    echo "CC = gcc" > Makefile
    echo "CFLAGS = -Wall -O2" >> Makefile
    echo "" >> Makefile
    echo "all: libmalcrypt.so" >> Makefile
    echo "" >> Makefile
    echo "libmalcrypt.so: cipher.o" >> Makefile
    echo "	\$(CC) -shared -o \$@ \$^" >> Makefile
    echo "" >> Makefile
    # Use awk to print %.o: %.c so Apptainer doesn't parse it as a section
    awk 'BEGIN{print "%.o: %.c"}' >> Makefile
    echo "	\$(CC) \$(CFLAGS) -c \$< -o \$@" >> Makefile
    echo "" >> Makefile
    echo "clean:" >> Makefile
    echo "	rm -f *.o *.so" >> Makefile

    # Create Oracle
    cd /app
    cat << 'EOF' > oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

void decrypt_block(uint32_t v[2], const uint32_t k[4]) {
    uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*4;
    for (int i=0; i<4; i++) {
        v1 -= ((v0<<4) + k[2]) ^ (v0 + sum) ^ ((v0>>5) + k[3]);
        v0 -= ((v1<<4) + k[0]) ^ (v1 + sum) ^ ((v1>>5) + k[1]);
        sum -= delta;
    }
    v[0]=v0; v[1]=v1;
}

int main() {
    uint8_t buf[2048];
    size_t len = fread(buf, 1, sizeof(buf)-1, stdin);
    if (len % 8 != 0 || len == 0) {
        printf("INVALID\n");
        return 1;
    }
    uint32_t k[4] = {0x01234567, 0x89ABCDEF, 0xFEEDBACC, 0x09876543};
    for (size_t i=0; i<len; i+=8) {
        decrypt_block((uint32_t*)(buf+i), k);
    }

    buf[len] = 0;
    char *p = strstr((char*)buf, "payload=");
    if (p) {
        p += 8;
        char *end = strchr(p, '&');
        if (end) *end = 0;
        printf("%s\n", p);
        return 0;
    }
    printf("INVALID\n");
    return 1;
}
EOF
    gcc -O2 oracle.c -o oracle_decoder
    strip oracle_decoder
    rm oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user