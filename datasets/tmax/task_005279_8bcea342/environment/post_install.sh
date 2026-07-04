apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    apt-get install -y qemu-system-x86 socat netcat-openbsd cron gcc

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/vm
    mkdir -p /home/user/healthcheck
    mkdir -p /app

    touch /home/user/vm/alpine.qcow2

    cat << 'EOF' > /home/user/vm/start_vm.sh
#!/bin/bash
# Missing port forwarding config
qemu-system-x86_64 -m 256 -hda /home/user/vm/alpine.qcow2 -nographic -daemonize -net nic -net user
EOF
    chmod +x /home/user/vm/start_vm.sh

    cat << 'EOF' > /home/user/healthcheck/wrapper.sh
#!/bin/sh
cat /home/user/healthcheck/raw_metrics.txt | /home/user/sanitizer | nc localhost 8080 > /home/user/healthcheck/last_result.txt
EOF
    chmod +x /home/user/healthcheck/wrapper.sh

    echo "* * * * * /home/user/healthcheck/wrapper.sh" | crontab -

    cat << 'EOF' > /app/oracle_sanitizer.c
#include <stdio.h>
#include <ctype.h>

int main() {
    int c;
    int in_underscore = 0;
    int first_char = 1;
    char buf[100000];
    int len = 0;

    while ((c = getchar()) != EOF) {
        if (isalnum(c)) {
            buf[len++] = tolower(c);
            in_underscore = 0;
            first_char = 0;
        } else {
            if (!first_char && !in_underscore) {
                buf[len++] = '_';
                in_underscore = 1;
            }
        }
    }
    if (len > 0 && buf[len-1] == '_') {
        len--;
    }
    for (int i = 0; i < len; i++) {
        putchar(buf[i]);
    }
    return 0;
}
EOF
    gcc /app/oracle_sanitizer.c -o /app/oracle_sanitizer
    chmod +x /app/oracle_sanitizer

    chmod -R 777 /home/user