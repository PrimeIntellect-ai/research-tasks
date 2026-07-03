apt-get update && apt-get install -y python3 python3-pip gcc strace gdb bsdmainutils coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/telemetry.c
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file>\n", argv[0]);
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    unsigned char header[4];
    if (read(fd, header, 4) != 4) {
        close(fd);
        return 0; // Ignore short files
    }

    // Packet type 0x5C has a dynamic payload size defined by the second byte
    if (header[0] == 0x5C) {
        // BUG: If header[1] is 0, size becomes -1 (underflow)
        // malloc((size_t)-1) will fail and return NULL.
        int payload_size = header[1] - 1; 

        char *payload = malloc(payload_size);

        // BUG: Dereferencing NULL pointer if malloc failed
        payload[0] = header[2]; 

        if (read(fd, payload, payload_size) > 0) {
            // process payload
        }
        free(payload);
    } else {
        // Normal processing for other packet types
        char dummy[128];
        read(fd, dummy, sizeof(dummy));
    }

    close(fd);
    return 0;
}
EOF

    gcc -o /home/user/telemetry /home/user/telemetry.c

    mkdir -p /home/user/packets
    cd /home/user/packets

    # Generate 200 normal packets
    for i in $(seq 1 200); do
        head -c 16 /dev/urandom > $(printf "%03d.bin" $i)
        # Ensure they don't accidentally start with 0x5C
        printf "\x01\x02\x03\x04" | dd of=$(printf "%03d.bin" $i) bs=4 count=1 conv=notrunc 2>/dev/null
    done

    # Generate 3 crash-triggering packets
    printf "\x5C\x00\xFF\xFF\x00\x00" > 042.bin
    printf "\x5C\x00\x1A\x2B\x00\x00" > 137.bin
    printf "\x5C\x00\x99\x88\x00\x00" > 199.bin

    chmod -R 777 /home/user