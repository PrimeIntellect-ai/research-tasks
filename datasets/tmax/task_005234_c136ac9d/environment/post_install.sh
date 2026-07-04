apt-get update && apt-get install -y python3 python3-pip gcc binutils coreutils
pip3 install pytest pexpect

mkdir -p /app

# Create the C source code for the legacy binary
cat << 'EOF' > /app/data_processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    char buf[8192];

    printf("Enter service PIN:\n");
    fflush(stdout);

    if (!fgets(buf, sizeof(buf), stdin)) return 1;
    buf[strcspn(buf, "\r\n")] = 0;
    if (strcmp(buf, "7734") != 0) return 1;

    printf("Enable fast mode? (y/n):\n");
    fflush(stdout);

    if (!fgets(buf, sizeof(buf), stdin)) return 1;

    ssize_t n;
    while ((n = read(0, buf, sizeof(buf))) > 0) {
        if (n != 4096) {
            usleep(2000);
        }
        for (ssize_t i = 0; i < n; i++) {
            buf[i] ^= 0xAA;
        }
        ssize_t written = 0;
        while (written < n) {
            ssize_t w = write(1, buf + written, n - written);
            if (w <= 0) return 1;
            written += w;
        }
    }
    return 0;
}
EOF

# Compile and strip the binary
gcc -O2 /app/data_processor.c -o /app/data_processor
strip /app/data_processor
rm /app/data_processor.c

# Generate the 50MB dataset
dd if=/dev/urandom of=/app/dataset.bin bs=1M count=50

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user