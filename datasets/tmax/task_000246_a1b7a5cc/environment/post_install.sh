apt-get update && apt-get install -y python3 python3-pip gcc imagemagick fonts-dejavu-core tesseract-ocr
    pip3 install pytest

    mkdir -p /app

    # Create the specification image
    convert -size 800x100 xc:white -font DejaVu-Sans -pointsize 18 -fill black -draw "text 10,50 'OP_ADD=0x10 OP_SUB=0x11 OP_MUL=0x12 OP_PUSH=0x20 OP_POP=0x30 CONST_MOD=65537'" /app/spec.png

    # Create the oracle program
    cat << 'EOF' > /app/oracle_vm.c
#include <stdio.h>
#include <stdint.h>

#define CONST_MOD 65537

int main() {
    int32_t stack[1024];
    int sp = 0;
    int c;
    while ((c = getchar()) != EOF) {
        if (c == 0x20) { // OP_PUSH
            int32_t val = 0;
            int b0 = getchar(); if (b0 == EOF) break;
            int b1 = getchar(); if (b1 == EOF) break;
            int b2 = getchar(); if (b2 == EOF) break;
            int b3 = getchar(); if (b3 == EOF) break;
            val = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24);
            if (sp < 1024) stack[sp++] = val;
        } else if (c == 0x10) { // OP_ADD
            if (sp >= 2) {
                int32_t v1 = stack[--sp];
                int32_t v2 = stack[--sp];
                int64_t res = (int64_t)v2 + v1;
                res %= CONST_MOD;
                if (res < 0) res += CONST_MOD;
                stack[sp++] = (int32_t)res;
            }
        } else if (c == 0x11) { // OP_SUB
            if (sp >= 2) {
                int32_t v1 = stack[--sp];
                int32_t v2 = stack[--sp];
                int64_t res = (int64_t)v2 - v1;
                res %= CONST_MOD;
                if (res < 0) res += CONST_MOD;
                stack[sp++] = (int32_t)res;
            }
        } else if (c == 0x12) { // OP_MUL
            if (sp >= 2) {
                int32_t v1 = stack[--sp];
                int32_t v2 = stack[--sp];
                int64_t res = (int64_t)v2 * v1;
                res %= CONST_MOD;
                if (res < 0) res += CONST_MOD;
                stack[sp++] = (int32_t)res;
            }
        } else if (c == 0x30) { // OP_POP
            if (sp > 0) sp--;
        }
    }
    if (sp > 0) {
        printf("%d\n", stack[sp-1]);
    } else {
        printf("0\n");
    }
    return 0;
}
EOF

    gcc -O3 /app/oracle_vm.c -o /app/oracle_vm
    rm /app/oracle_vm.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user