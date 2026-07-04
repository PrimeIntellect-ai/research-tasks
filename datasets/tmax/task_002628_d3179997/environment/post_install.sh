apt-get update && apt-get install -y python3 python3-pip gcc gdb valgrind libc6-dbg
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/log_processor.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void parse_log_line(char *line) {
    // Expected format: TIMESTAMP|SEVERITY|MESSAGE
    char *delim1 = strchr(line, '|');
    if (!delim1) return;
    *delim1 = '\0';

    char *delim2 = strchr(delim1 + 1, '|');
    if (!delim2) return;
    *delim2 = '\0';

    char *timestamp = line;
    char *severity = delim1 + 1;
    char *message = delim2 + 1;

    // Strip trailing newline from message
    int len = strlen(message);
    if (len > 0 && message[len-1] == '\n') {
        message[len-1] = '\0';
        len--;
    }

    // Check for line continuation escape character at the end of the message
    if (message[len-1] == '\\') {
        printf("CONTINUATION: %s\n", timestamp);
    } else {
        printf("PROCESSED: [%s] %s\n", severity, message);
    }
}

int main() {
    char buffer[512];
    while (fgets(buffer, sizeof(buffer), stdin)) {
        parse_log_line(buffer);
    }
    return 0;
}
EOF

    chmod -R 777 /home/user