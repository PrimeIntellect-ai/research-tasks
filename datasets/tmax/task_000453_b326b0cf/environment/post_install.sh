apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    mkdir -p /app/backup-metric-parser-1.0.0

    cat << 'EOF' > /app/backup-metric-parser-1.0.0/main.c
#include <stdio.h>

int main() {
    char mount[256];
    long long used, total;
    if (scanf("%255s %lld %lld", mount, &used, &total) == 3) {
        float usage = (float)used / (float)total;
        printf("backup_mount_usage{mount=\"%s\"} %f\n", mount, usage);
    }
    return 0;
}
EOF

    cat << 'EOF' > /app/backup-metric-parser-1.0.0/Makefile
CC=my-gcc-99
CFLAGS=-O2

parser: main.c
	$(CC) $(CFLAGS) -o parser main.c
EOF

    mkdir -p /opt/oracle
    gcc -O2 -o /opt/oracle/backup_parser_oracle /app/backup-metric-parser-1.0.0/main.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user