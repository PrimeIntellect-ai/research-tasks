apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/workspace
    cd /home/user/workspace

    cat << 'EOF' > decrypt_tool.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
/* BUG: Missing include for uint8_t */

void generate_dump() {
    uint8_t memory[256];
    for(int i=0; i<256; i++) {
        memory[i] = (uint8_t)(sqrt(i) + i);
    }

    const char* secret = "SEC_99x_DEADLOCK";
    for(int i=0; i<16; i++) {
        memory[100+i] = secret[i] ^ (i + 5);
    }

    FILE *f = fopen("mem.dmp", "wb");
    fwrite(memory, 1, 256, f);
    fclose(f);
}

int main() {
    generate_dump();
    return 0;
}
EOF

    cat << 'EOF' > Makefile
all:
	gcc decrypt_tool.c -o decrypt_tool
EOF

    cat << 'EOF' > analyze_dump.py
import struct

def extract():
    with open("mem.dmp", "rb") as f:
        data = f.read()

    extracted = []
    # BUG: Off-by-one (15 instead of 16) and incorrect formula (i+4 instead of i+5)
    for i in range(15): 
        val = data[100 + i]
        decrypted = val ^ (i + 4)
        extracted.append(chr(decrypted))

    with open("/home/user/flag.txt", "w") as f:
        f.write("".join(extracted))

if __name__ == "__main__":
    extract()
EOF

    chmod -R 777 /home/user