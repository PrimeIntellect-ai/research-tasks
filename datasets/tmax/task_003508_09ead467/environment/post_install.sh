apt-get update && apt-get install -y python3 python3-pip gcc e2tools e2fsprogs sleuthkit
    pip3 install pytest

    mkdir -p /home/user
    mkdir -p /app

    # Create gold lines
    for i in $(seq 1 50); do
        echo "Log entry line number $i with some random data $RANDOM, and more data" >> /tmp/gold_lines.txt
    done

    # Create ext4 image and simulate deleted file
    dd if=/dev/zero of=/home/user/logs.img bs=1M count=10
    mkfs.ext4 -F /home/user/logs.img
    e2cp /tmp/gold_lines.txt /home/user/logs.img:/trace.log
    e2rm /home/user/logs.img:/trace.log

    # Create sign_log binary
    cat << 'EOF' > /tmp/sign_log.c
#include <stdio.h>
int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    int sum = 0;
    for (int i = 0; argv[1][i]; i++) sum += argv[1][i];
    printf("%04X\n", sum ^ 0x5A);
    return 0;
}
EOF
    gcc -O2 -s /tmp/sign_log.c -o /app/sign_log
    chmod 755 /app/sign_log

    # Create buggy repair.c
    cat << 'EOF' > /home/user/repair.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    FILE *f = fopen("trace.log", "r");
    if (!f) {
        printf("Failed to open trace.log\n");
        return 1;
    }
    char buf[1024];
    while (fgets(buf, sizeof(buf), f)) {
        int len = strlen(buf);
        if (len > 0 && buf[len-1] == '\n') {
            buf[len] = '\0'; // Off-by-one bug
        }
        int i = 0;
        while (buf[i]) {
            if (buf[i] == ',') {
                continue; // Infinite loop bug
            }
            i++;
        }
        // Missing logic to sign and output
    }
    fclose(f);
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user