apt-get update && apt-get install -y python3 python3-pip gcc binutils cargo rustc
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /tmp/auth_encoder.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char cb64[]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

void encodeblock(unsigned char *in, unsigned char *out, int len) {
    out[0] = cb64[in[0] >> 2];
    out[1] = cb64[((in[0] & 0x03) << 4) | ((in[1] & 0xf0) >> 4)];
    out[2] = (unsigned char) (len > 1 ? cb64[((in[1] & 0x0f) << 2) | ((in[2] & 0xc0) >> 6)] : '=');
    out[3] = (unsigned char) (len > 2 ? cb64[in[2] & 0x3f] : '=');
}

int main(int argc, char *argv[]) {
    if (argc != 3) return 1;
    if (strcmp(argv[1], "6184") != 0) {
        printf("Auth failed\n");
        return 1;
    }

    char *pin = argv[1];
    char *input = argv[2];
    int len = strlen(input);

    unsigned char *xor_data = malloc(len);
    for(int i = 0; i < len; i++) {
        xor_data[i] = input[i] ^ pin[i % 4];
    }

    unsigned char in[3], out[4];
    int i = 0;
    while (i < len) {
        int chunk_len = 0;
        for (int j = 0; j < 3; j++) {
            if (i < len) {
                in[j] = xor_data[i++];
                chunk_len++;
            } else {
                in[j] = 0;
            }
        }
        encodeblock(in, out, chunk_len);
        printf("%c%c%c%c", out[0], out[1], out[2], out[3]);
    }
    free(xor_data);
    return 0;
}
EOF

    gcc -O3 /tmp/auth_encoder.c -o /app/auth_encoder
    strip -s /app/auth_encoder
    chmod +x /app/auth_encoder

    cat << 'EOF' > /usr/local/bin/oracle_wrapper.sh
#!/bin/bash
/app/auth_encoder 6184 "$1"
EOF
    chmod +x /usr/local/bin/oracle_wrapper.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user