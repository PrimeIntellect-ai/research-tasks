apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    # Create directories
    mkdir -p /opt/oracle
    mkdir -p /app/doctar-1.0/src

    # Create oracle source code
    cat << 'EOF' > /opt/oracle/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void normalize_doc_path(const char* input, char* output) {
    char* stack[2048];
    int top = 0;
    char* copy = strdup(input);
    int is_absolute = (input[0] == '/');

    char* token = copy;
    char* next;
    while (*token) {
        while (*token == '/') token++;
        if (!*token) break;
        next = token;
        while (*next && *next != '/') next++;
        char saved = *next;
        *next = '\0';

        if (strcmp(token, ".") == 0) {
            // skip
        } else if (strcmp(token, "..") == 0) {
            if (top > 0 && strcmp(stack[top-1], "..") != 0) {
                free(stack[--top]);
            } else if (!is_absolute) {
                stack[top++] = strdup("..");
            }
        } else {
            stack[top++] = strdup(token);
        }

        *next = saved;
        token = next;
    }

    output[0] = '\0';
    if (is_absolute) {
        strcat(output, "/");
    }
    for (int i = 0; i < top; i++) {
        strcat(output, stack[i]);
        if (i < top - 1) {
            strcat(output, "/");
        }
        free(stack[i]);
    }
    if (strlen(output) == 0 && !is_absolute) {
        strcat(output, ".");
    }
    free(copy);
}

int main(int argc, char** argv) {
    if (argc < 2) return 0;
    char output[8192];
    normalize_doc_path(argv[1], output);
    printf("%s\n", output);
    return 0;
}
EOF

    # Compile oracle and clean up source
    gcc -O2 /opt/oracle/oracle.c -o /opt/oracle/doctar_oracle
    chmod +x /opt/oracle/doctar_oracle
    rm /opt/oracle/oracle.c

    # Create doctar project files
    cat << 'EOF' > /app/doctar-1.0/Makefile
CC = gcc
CFLAGS = -Wall -I/nonexistent/include
TARGET = doctar_sanitize

all: $(TARGET)

$(TARGET): src/main.c src/sanitize.c
	$(CC) $(CFLAGS) -o $(TARGET) src/main.c src/sanitize.c

clean:
	rm -f $(TARGET)
EOF

    cat << 'EOF' > /app/doctar-1.0/src/sanitize.h
#ifndef SANITIZE_H
#define SANITIZE_H

void normalize_doc_path(const char* input, char* output);

#endif
EOF

    cat << 'EOF' > /app/doctar-1.0/src/sanitize.c
#include "sanitize.h"
#include <string.h>

void normalize_doc_path(const char* input, char* output) {
    // BUG: stubbed out, does not sanitize
    strcpy(output, input);
}
EOF

    cat << 'EOF' > /app/doctar-1.0/src/main.c
#include <stdio.h>
#include "sanitize.h"

int main(int argc, char** argv) {
    if (argc < 2) return 0;
    char output[8192];
    normalize_doc_path(argv[1], output);
    printf("%s\n", output);
    return 0;
}
EOF

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app