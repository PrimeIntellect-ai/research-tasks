apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest fastapi uvicorn

    mkdir -p /app/liburldecode
    mkdir -p /opt/oracle

    # Create the vulnerable urldecode.c for the agent
    cat << 'EOF' > /app/liburldecode/urldecode.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char hex_to_char(char c1, char c2) {
    char hex[3] = {c1, c2, 0};
    return (char)strtol(hex, NULL, 16);
}

void urldecode(const char *src, char *dest) {
    int i = 0, j = 0;
    int len = strlen(src);
    while (i < len) {
        if (src[i] == '%') {
            dest[j++] = hex_to_char(src[i+1], src[i+2]);
            i += 3;
        } else {
            dest[j++] = src[i++];
        }
    }
    dest[j] = '\0';
}

#ifdef CLI
int main(int argc, char **argv) {
    if (argc < 2) return 0;
    char *out = malloc(strlen(argv[1]) + 1);
    urldecode(argv[1], out);
    printf("%s", out);
    free(out);
    return 0;
}
#endif
EOF

    # Create the broken Makefile for the agent
    cat << 'EOF' > /app/liburldecode/Makefile
CC=gcc
CFLAGS=-Wall -Werror

all: decode_cli liburldecode.so

decode_cli: urldecode.c
	$(CC) $(CFLAGS) -DCLI urldecode.c -o decode_cli

liburldecode.so: urldecode.c
	$(CC) $(CFLAGS) -shared urldecode.c -o liburldecode.so

clean:
	rm -f decode_cli liburldecode.so
EOF

    # Create the secure oracle urldecode.c
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int is_hex(char c) {
    return (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
}

char hex_to_char(char c1, char c2) {
    char hex[3] = {c1, c2, 0};
    return (char)strtol(hex, NULL, 16);
}

void urldecode(const char *src, char *dest) {
    int i = 0, j = 0;
    int len = strlen(src);
    while (i < len) {
        if (src[i] == '%' && i + 2 < len && is_hex(src[i+1]) && is_hex(src[i+2])) {
            dest[j++] = hex_to_char(src[i+1], src[i+2]);
            i += 3;
        } else {
            dest[j++] = src[i++];
        }
    }
    dest[j] = '\0';
}

#ifdef CLI
int main(int argc, char **argv) {
    if (argc < 2) return 0;
    char *out = malloc(strlen(argv[1]) + 1);
    urldecode(argv[1], out);
    printf("%s", out);
    free(out);
    return 0;
}
#endif
EOF

    # Compile the oracle binary
    gcc -Wall -Werror -DCLI /tmp/oracle.c -o /opt/oracle/decode_cli
    rm /tmp/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app