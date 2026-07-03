apt-get update && apt-get install -y python3 python3-pip gcc make git curl
    pip3 install pytest

    mkdir -p /app
    cd /app
    git clone --branch v1.7.15 https://github.com/DaveGamble/cJSON.git
    cd cJSON
    sed -i 's/#include <stdio.h>/#include <stdio_broken.h>/' cJSON.c

    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

void error_exit() {
    printf("{\"error\": \"invalid format\"}\n");
    exit(1);
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) error_exit();

    uint8_t magic[4];
    if (fread(magic, 1, 4, f) != 4) error_exit();
    if (memcmp(magic, "ARTF", 4) != 0) error_exit();

    uint8_t version;
    if (fread(&version, 1, 1, f) != 1) error_exit();
    if (version != 1) error_exit();

    uint8_t flags;
    if (fread(&flags, 1, 1, f) != 1) error_exit();

    uint16_t meta_len;
    if (fread(&meta_len, 2, 1, f) != 1) error_exit();

    uint32_t payload_len;
    if (fread(&payload_len, 4, 1, f) != 1) error_exit();

    char *meta = malloc(meta_len + 1);
    if (meta_len > 0 && fread(meta, 1, meta_len, f) != meta_len) error_exit();
    meta[meta_len] = '\0';

    uint8_t *payload = malloc(payload_len);
    if (payload_len > 0 && fread(payload, 1, payload_len, f) != payload_len) error_exit();

    printf("{\"metadata\":{");
    char *start = meta;
    int first = 1;
    while(start < meta + meta_len) {
        char *end = strchr(start, ';');
        if (!end) end = meta + meta_len;

        char *colon = memchr(start, ':', end - start);
        if (colon) {
            if (!first) printf(",");
            first = 0;
            printf("\"");
            for(char *c = start; c < colon; c++) {
                if (*c == '"' || *c == '\\') printf("\\%c", *c);
                else printf("%c", *c);
            }
            printf("\":\"");
            for(char *c = colon + 1; c < end; c++) {
                if (*c == '"' || *c == '\\') printf("\\%c", *c);
                else printf("%c", *c);
            }
            printf("\"");
        }
        start = end;
        if (*start == ';') start++;
    }

    uint8_t checksum = 0;
    for(uint32_t i=0; i<payload_len; i++) {
        uint8_t b = payload[i];
        if (flags & 1) b ^= 0x5A;
        checksum += b;
    }

    printf("},\"payload_size\":%u,\"payload_checksum\":%u}\n", payload_len, checksum);
    return 0;
}
EOF

    gcc -O3 -static /opt/oracle/oracle.c -o /opt/oracle/abc_parser_oracle
    strip /opt/oracle/abc_parser_oracle
    rm /opt/oracle/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user