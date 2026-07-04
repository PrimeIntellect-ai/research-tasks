apt-get update && apt-get install -y \
        python3 python3-pip \
        ffmpeg \
        protobuf-compiler \
        protobuf-c-compiler \
        libprotobuf-c-dev \
        libssl-dev \
        gcc \
        make \
        pkg-config

    pip3 install pytest protobuf

    mkdir -p /app
    mkdir -p /home/user/legacy_parser

    # Create dummy video file
    touch /app/api_traffic.mp4

    # Create api_schema.proto
    cat << 'EOF' > /home/user/api_schema.proto
syntax = "proto3";
message ApiRequest {
  string endpoint = 1;
  bytes raw_payload = 2;
  int32 timestamp = 3;
}
EOF

    # Create main.c
    cat << 'EOF' > /home/user/legacy_parser/main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>
#include "api_schema.pb-c.h"

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    uint8_t *buf = malloc(len);
    fread(buf, 1, len, f);
    fclose(f);

    ApiRequest *req = api_request__unpack(NULL, len, buf);
    if (!req) {
        free(buf);
        return 1;
    }

    if (req->raw_payload.len > 0) {
        uint8_t *payload = req->raw_payload.data;
        size_t plen = req->raw_payload.len;
        uint8_t *rev = malloc(plen);
        for (size_t i = 0; i < plen; i++) {
            rev[i] = payload[plen - 1 - i];
        }
        unsigned char md5[MD5_DIGEST_LENGTH];
        MD5(rev, plen, md5);
        for(int i=0; i<MD5_DIGEST_LENGTH; i++) {
            printf("%02x", md5[i]);
        }
        printf("\n");
        free(rev);
    } else {
        unsigned char md5[MD5_DIGEST_LENGTH];
        MD5(NULL, 0, md5);
        for(int i=0; i<MD5_DIGEST_LENGTH; i++) {
            printf("%02x", md5[i]);
        }
        printf("\n");
    }

    api_request__free_unpacked(req, NULL);
    free(buf);
    return 0;
}
EOF

    # Create broken Makefile
    cat << 'EOF' > /home/user/legacy_parser/Makefile
payload_parser: main.c
    gcc -o payload_parser main.c ../api_schema.pb-c.c -I.. -lprotobuf-c -lcrypto
EOF

    # Compile reference parser
    cd /home/user
    protoc-c --c_out=. api_schema.proto
    gcc -o /app/reference_parser legacy_parser/main.c api_schema.pb-c.c -I. -lprotobuf-c -lcrypto
    cd /

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app