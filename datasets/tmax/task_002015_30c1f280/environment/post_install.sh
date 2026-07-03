apt-get update && apt-get install -y python3 python3-pip gcc strace binutils
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /tmp/wal.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;

    while (1) {
        uint32_t magic;
        if (fread(&magic, 1, 4, f) != 4) break;
        if (magic != 0xDEADBEEF) {
            fseek(f, -3, SEEK_CUR);
            continue;
        }

        uint16_t L;
        if (fread(&L, 1, 2, f) != 2) break;

        long pos = ftell(f);
        fseek(f, 0, SEEK_END);
        long end = ftell(f);
        fseek(f, pos, SEEK_SET);

#ifdef BUG
        if (pos + L + 1 > end) {
            while(1) {}
        }
#else
        if (pos + L + 1 > end) {
            break;
        }
#endif

        char *payload = malloc(L + 1);
        if (fread(payload, 1, L, f) != L) {
            free(payload);
            break;
        }
        payload[L] = '\0';

        uint8_t checksum;
        if (fread(&checksum, 1, 1, f) != 1) {
            free(payload);
            break;
        }

        uint8_t calc_checksum = 0;
        for (int i = 0; i < L; i++) {
            calc_checksum ^= (uint8_t)payload[i];
        }

        if (calc_checksum == checksum) {
            printf("{\"record\": \"%s\"}\n", payload);
        }
        free(payload);
    }
    fclose(f);
    return 0;
}
EOF

    gcc -O2 -DBUG /tmp/wal.c -o /app/wal_recovery_tool
    strip /app/wal_recovery_tool

    gcc -O2 /tmp/wal.c -o /app/wal_recovery_tool_oracle
    strip /app/wal_recovery_tool_oracle

    rm /tmp/wal.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user