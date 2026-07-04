apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    mkdir -p /app/loc-processor-1.0.0

    # Create vendored package files
    cat << 'EOF' > /app/loc-processor-1.0.0/Makefile
CC = gcc
CFLAGS = -Wall -DFAIL_DEDUP=1
OBJS = main.o dedup.o

loc_tool: $(OBJS)
	$(CC) $(CFLAGS) -o loc_tool $(OBJS)

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

dedup.o: dedup.c
	$(CC) $(CFLAGS) -c dedup.c

join.o: join.c
	$(CC) $(CFLAGS) -c join.c
EOF

    cat << 'EOF' > /app/loc-processor-1.0.0/main.c
int main() { return 0; }
EOF

    cat << 'EOF' > /app/loc-processor-1.0.0/dedup.c
void dedup() {}
EOF

    cat << 'EOF' > /app/loc-processor-1.0.0/join.c
void join() {}
EOF

    # Create oracle formatter
    cat << 'EOF' > /app/oracle_formatter.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_line(char *line) {
    char *tokens[5];
    for (int i = 0; i < 5; i++) tokens[i] = "";

    int tok_idx = 0;
    char *start = line;
    for (char *p = line; *p; p++) {
        if (*p == '\n' || *p == '\r') {
            *p = '\0';
            tokens[tok_idx++] = start;
            break;
        }
        if (*p == ',') {
            *p = '\0';
            tokens[tok_idx++] = start;
            start = p + 1;
            if (tok_idx == 5) break;
        }
    }
    if (tok_idx < 5 && *start != '\0') {
        tokens[tok_idx] = start;
    }

    char *timestamp = tokens[0];
    char *k = tokens[1];
    char *langs[3] = {tokens[2], tokens[3], tokens[4]};
    char *lang_names[3] = {"lang_es", "lang_fr", "lang_de"};

    char *t_ptr = strchr(timestamp, 'T');
    if (t_ptr) {
        char *colon1 = strchr(t_ptr, ':');
        if (colon1) {
            char *colon2 = strchr(colon1 + 1, ':');
            if (colon2) {
                strcpy(colon1, ":00:00");
            } else {
                strcpy(colon1, ":00:00");
            }
        }
    }

    for (int i = 0; i < 3; i++) {
        if (strlen(langs[i]) > 0) {
            printf("%s,%s,%s,%s\n", timestamp, k, lang_names[i], langs[i]);
        }
    }
}

int main() {
    char line[2048];
    while (fgets(line, sizeof(line), stdin)) {
        process_line(line);
    }
    return 0;
}
EOF

    gcc -O3 -o /app/oracle_formatter /app/oracle_formatter.c
    strip /app/oracle_formatter
    chmod +x /app/oracle_formatter
    rm /app/oracle_formatter.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user