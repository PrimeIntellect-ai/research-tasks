apt-get update && apt-get install -y python3 python3-pip git gcc
pip3 install pytest

git config --global user.name "Setup"
git config --global user.email "setup@example.com"

mkdir -p /home/user/telemetry_decoder
cd /home/user/telemetry_decoder
git init

# Commit 1
cat << 'EOF' > main.c
#include <stdio.h>
#include <stdint.h>
int main() {
    uint32_t payload[2];
    if (fread(payload, 1, 8, stdin) != 8) return 0;
    printf("Decoded: %u\n", payload[1]);
    return 0;
}
EOF
git add main.c && git commit -m "Initial commit"

# Commit 2
cat << 'EOF' > main.c
#include <stdio.h>
#include <stdint.h>
int main() {
    uint32_t payload[2];
    if (fread(payload, 1, 8, stdin) != 8) return 0;
    if (payload[0] == 0) return 1;
    printf("Decoded: %u\n", payload[1]);
    return 0;
}
EOF
git add main.c && git commit -m "Add ID check"

# Commit 3 (BAD COMMIT)
cat << 'EOF' > main.c
#include <stdio.h>
#include <stdint.h>
int main() {
    uint32_t payload[2];
    if (fread(payload, 1, 8, stdin) != 8) return 0;
    if (payload[0] == 0) return 1;
    // simulate encoding issue: float precision loss
    float temp = (float)payload[1];
    uint32_t recovered = (uint32_t)temp;
    if (recovered != payload[1]) {
        if (payload[1] == 0x7FFFFFFF) {
            char *p = NULL;
            *p = 1; // CRASH
        }
    }
    printf("Decoded: %u\n", payload[1]);
    return 0;
}
EOF
git add main.c && git commit -m "Optimize decoding using float math"
BAD_HASH=$(git rev-parse HEAD)
echo $BAD_HASH > /tmp/expected_bad_commit.txt

# Commit 4
cat << 'EOF' > main.c
#include <stdio.h>
#include <stdint.h>
int main() {
    uint32_t payload[2];
    if (fread(payload, 1, 8, stdin) != 8) return 0;
    if (payload[0] == 0) return 1;
    float temp = (float)payload[1];
    uint32_t recovered = (uint32_t)temp;
    if (recovered != payload[1]) {
        if (payload[1] == 0x7FFFFFFF) {
            char *p = NULL;
            *p = 1; // CRASH
        }
    }
    printf("Decoded payload %u with val: %u\n", payload[0], payload[1]);
    return 0;
}
EOF
git add main.c && git commit -m "Update print statement"

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod 777 /tmp/expected_bad_commit.txt