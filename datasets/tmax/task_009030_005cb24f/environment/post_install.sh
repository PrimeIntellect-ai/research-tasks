apt-get update && apt-get install -y python3 python3-pip git gcc gdb
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/malware_repo
    cd /home/user/malware_repo

    git init

    cat << 'EOF' > malware.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SECRET "gh0st_1n_th3_sh3ll"

void check_payload(const char *payload) {
    struct {
        char buf[32];
        unsigned int magic;
    } data;

    data.magic = 0x0;
    // VULNERABILITY: strcpy into a fixed buffer
    strcpy(data.buf, payload);

    if (data.magic == 0x8BADF00D) {
        printf("Backdoor triggered!\n");
    } else {
        printf("Safe.\n");
    }
}

int main(int argc, char **argv) {
    if (argc != 3) {
        printf("Usage: %s <auth> <file>\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], SECRET) != 0) {
        printf("Auth failed.\n");
        return 1;
    }

    FILE *f = fopen(argv[2], "rb");
    if (!f) return 1;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *p = malloc(len + 1);
    fread(p, 1, len, f);
    p[len] = '\0';
    fclose(f);

    check_payload(p);
    free(p);
    return 0;
}
EOF

    git config user.email "dev@malware.local"
    git config user.name "Dev"
    git add malware.c
    git commit -m "Initial commit of parsing tool"

    sed -i 's/#define SECRET "gh0st_1n_th3_sh3ll"/#define SECRET getenv("AUTH_TOKEN")/' malware.c
    git add malware.c
    git commit -m "Remove hardcoded secret, use env var"

    gcc -g -fno-stack-protector -z execstack malware.c -o malware
    chmod +x malware

    chown -R user:user /home/user/malware_repo
    chmod -R 777 /home/user