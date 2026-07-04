apt-get update && apt-get install -y python3 python3-pip gcc binutils coreutils
    pip3 install pytest

    # Create the target IDS binary
    mkdir -p /app
    cat << 'EOF' > /app/target_ids.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    if(argc != 2) return 0;
    FILE* fp = fopen(argv[1], "rb");
    if(!fp) return 0;
    char buf[4096] = {0};
    size_t n = fread(buf, 1, 4095, fp);
    fclose(fp);

    int blocked = 0;

    // Rule 1: ELF
    if(n > 32 && buf[0] == 0x7f && buf[1] == 'E' && buf[2] == 'L' && buf[3] == 'F') {
        unsigned int ep = *(unsigned int*)(&buf[24]); 
        if(ep == 0x08049999) {
            for(size_t i=0; i<n-6; i++) {
                if(memcmp(&buf[i], ".pwned", 6) == 0) blocked = 1;
            }
        }
    }

    // Rule 2: TLS
    if(strstr(buf, "-----BEGIN CERTIFICATE-----") && strstr(buf, "O=RogueAPT CA")) {
        blocked = 1;
    }

    // Rule 3: XSS
    char* p = strstr(buf, "<svg onload=");
    if(p) {
        char* p2 = strstr(p, "atob(");
        if(p2 && (p2 - p) <= 20) {
            blocked = 1;
        }
    }

    if(blocked) {
        printf("BLOCKED\n");
        return 1;
    }
    printf("ALLOWED\n");
    return 0;
}
EOF
    gcc -O2 /app/target_ids.c -o /app/target_ids
    strip -s /app/target_ids
    rm /app/target_ids.c

    # Create training data
    mkdir -p /home/user/training_data/blocked
    mkdir -p /home/user/training_data/allowed

    # Blocked examples
    printf "\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x03\x00\x01\x00\x00\x00\x99\x99\x04\x08\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00.pwned" > /home/user/training_data/blocked/elf_bad.bin
    echo "-----BEGIN CERTIFICATE-----\nO=RogueAPT CA\n" > /home/user/training_data/blocked/tls_bad.pem
    echo "<html><body><svg onload=atob('WFNT')></body></html>" > /home/user/training_data/blocked/xss_bad.html

    # Allowed examples
    printf "\x7fELF\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x03\x00\x01\x00\x00\x00\x00\x00\x00\x00" > /home/user/training_data/allowed/elf_ok.bin
    echo "-----BEGIN CERTIFICATE-----\nO=Good CA\n" > /home/user/training_data/allowed/tls_ok.pem
    echo "<html><body><svg onload=alert(1)></body></html>" > /home/user/training_data/allowed/xss_ok.html

    # Setup user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user