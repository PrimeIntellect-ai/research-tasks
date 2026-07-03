apt-get update && apt-get install -y python3 python3-pip golang gcc binutils strace
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app
    cat << 'EOF' > /tmp/provtool.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    char line[256];
    int unsafe = 0;
    while (fgets(line, sizeof(line), f)) {
        char key[256], val[256];
        if (sscanf(line, "%255[^:]: %255[^\n]", key, val) == 2) {
            if (strcmp(key, "Target-Dir") == 0) {
                if (strstr(val, "../") || strncmp(val, "/etc", 4) == 0) {
                    unsafe = 1;
                }
            } else if (strcmp(key, "Disk-Quota") == 0) {
                int quota = atoi(val);
                if (quota < 0) {
                    unsafe = 1;
                } else if (quota > 10000) {
                    char *crash = NULL;
                    *crash = 1;
                }
            } else if (strcmp(key, "Ssh-Key-Auth") == 0) {
                if (strcmp(val, "false") == 0) {
                    unsafe = 1;
                }
            }
        }
    }
    fclose(f);

    if (unsafe) {
        // Silently apply unsafe settings
        return 0;
    }
    return 0;
}
EOF
    gcc -O2 /tmp/provtool.c -o /app/provtool
    strip /app/provtool

    mkdir -p /home/user/examples/clean
    mkdir -p /home/user/examples/evil

    cat << 'EOF' > /home/user/examples/clean/1.txt
Target-Dir: /mnt/data/test
Disk-Quota: 100
Ssh-Key-Auth: true
EOF

    cat << 'EOF' > /home/user/examples/clean/2.txt
Target-Dir: /var/www/html
Disk-Quota: 5000
Ssh-Key-Auth: true
EOF

    cat << 'EOF' > /home/user/examples/clean/3.txt
Target-Dir: /mnt/data/app
Disk-Quota: 0
Ssh-Key-Auth: true
EOF

    cat << 'EOF' > /home/user/examples/evil/1.txt
Target-Dir: /etc/passwd
Disk-Quota: 100
Ssh-Key-Auth: true
EOF

    cat << 'EOF' > /home/user/examples/evil/2.txt
Target-Dir: /mnt/data/test
Disk-Quota: -1
Ssh-Key-Auth: true
EOF

    cat << 'EOF' > /home/user/examples/evil/3.txt
Target-Dir: /mnt/data/test
Disk-Quota: 10001
Ssh-Key-Auth: true
EOF

    chmod -R 777 /home/user