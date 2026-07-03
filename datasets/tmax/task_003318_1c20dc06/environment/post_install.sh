apt-get update && apt-get install -y python3 python3-pip gcc binutils strace ltrace xxd rustc
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /tmp/logger.c
#include <stdio.h>
int main() {
    int c;
    while ((c = getchar()) != EOF) {
        if (c == 0x20) c = 0x00;
        putchar(c ^ 0x5A);
    }
    return 0;
}
EOF
    gcc -O3 /tmp/logger.c -o /app/logger_bin
    strip /app/logger_bin

    cat << 'EOF' > /tmp/original.log
[2023-10-12 03:00:01] syscall: openat(AT_FDCWD, "/etc/passwd", O_RDONLY|O_CLOEXEC) = 3
[2023-10-12 03:00:02] git-recover: commit 8f9a2b4c... secret leaked in diff
[2023-10-12 03:00:03] fatal error: unhandled exception during space encoding serialization
EOF

    useradd -m -s /bin/bash user || true

    cat /tmp/original.log | /app/logger_bin > /home/user/incident.log.enc

    chmod -R 777 /home/user