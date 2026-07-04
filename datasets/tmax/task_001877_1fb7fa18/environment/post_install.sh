apt-get update && apt-get install -y python3 python3-pip gcc make espeak
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user/pipeline

    # Generate audio file
    espeak -w /app/alert.wav "The required telemetry offset is minus five hours."

    # Generate crash dump
    dd if=/dev/urandom of=/app/crash.dump bs=1M count=5
    echo "POISON_X9A2B4C1D" >> /app/crash.dump

    # Create oracle parser
    cat << 'EOF' > /app/oracle_parser.c
#define _XOPEN_SOURCE
#include <stdio.h>
#include <string.h>
#include <time.h>

int main() {
    char line[1024];
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (strstr(line, "POISON_X9A2B4C1D")) {
            printf("[DROPPED]\n");
            continue;
        }
        struct tm tm;
        memset(&tm, 0, sizeof(struct tm));
        char *ret = strptime(line, "%Y-%m-%d %H:%M:%S", &tm);
        if (ret != NULL && *ret == '\0') {
            tm.tm_hour -= 5;
            tm.tm_isdst = -1;
            mktime(&tm);
            char out[256];
            strftime(out, sizeof(out), "%Y-%m-%d %H:%M:%S", &tm);
            printf("%s\n", out);
        } else {
            printf("[ERROR]\n");
        }
    }
    return 0;
}
EOF
    gcc -o /app/oracle_parser /app/oracle_parser.c
    rm /app/oracle_parser.c

    # Create faulty Makefile
    cat << 'EOF' > /home/user/pipeline/Makefile
all:
cc -o parser parser.c
EOF

    # Create faulty parser.c
    cat << 'EOF' > /home/user/pipeline/parser.c
int main() {
    char line[256];
    fgets(line, 256, stdin);
    printf("Not implemented\n");
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app