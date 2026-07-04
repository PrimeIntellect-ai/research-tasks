apt-get update && apt-get install -y python3 python3-pip gcc espeak-ng
pip3 install pytest

mkdir -p /app

# Create the oracle reference implementation
cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define BLOCK_SIZE 4096

void reverse_block(uint8_t *block, size_t size) {
    size_t i, j;
    uint8_t temp;
    if (size == 0) return;
    for (i = 0, j = size - 1; i < j; i++, j--) {
        temp = block[i];
        block[i] = block[j];
        block[j] = temp;
    }
}

int main() {
    uint8_t header[16];
    if (fread(header, 1, 16, stdin) != 16) {
        return 1;
    }
    if (memcmp(header, "PATC", 4) != 0) {
        return 1;
    }
    uint32_t payload_length;
    memcpy(&payload_length, header + 4, 4);

    fwrite(header, 1, 16, stdout);

    uint8_t block[BLOCK_SIZE];
    uint32_t bytes_read = 0;
    while (bytes_read < payload_length) {
        size_t to_read = payload_length - bytes_read;
        if (to_read > BLOCK_SIZE) to_read = BLOCK_SIZE;
        size_t r = fread(block, 1, to_read, stdin);
        if (r != to_read) {
            return 1;
        }
        reverse_block(block, r);
        fwrite(block, 1, r, stdout);
        bytes_read += r;
    }
    return 0;
}
EOF

gcc -O3 /tmp/oracle.c -o /app/oracle_patch_transformer
rm /tmp/oracle.c

# Generate the audio configuration file
espeak-ng -w /app/arch_config.wav "The new memory alignment block size is four thousand ninety six bytes."

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user