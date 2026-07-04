apt-get update && apt-get install -y python3 python3-pip gcc binutils file
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_HISTORY 10000

typedef struct {
    long long ts;
    char key[64];
} Event;

Event history[MAX_HISTORY];
int hist_count = 0;

void hex_to_ascii_lower(const char* hex, char* ascii) {
    size_t len = strlen(hex);
    for (size_t i = 0; i < len; i += 2) {
        char byte[3] = {hex[i], hex[i+1], '\0'};
        char c = (char)strtol(byte, NULL, 16);
        ascii[i/2] = tolower(c);
    }
    ascii[len/2] = '\0';
}

int main() {
    char line[1024];
    while (fgets(line, sizeof(line), stdin)) {
        long long ts;
        char key[64];
        char hex[256];
        if (sscanf(line, "%lld\t%63[^\t]\t%255[^\n]", &ts, key, hex) == 3) {
            char ascii[128];
            hex_to_ascii_lower(hex, ascii);

            // Add to history
            if (hist_count < MAX_HISTORY) {
                history[hist_count].ts = ts;
                strcpy(history[hist_count].key, key);
                hist_count++;
            }

            // Calculate rolling window
            int count = 0;
            for (int i = 0; i < hist_count; i++) {
                if (history[i].ts >= ts - 60 && history[i].ts <= ts) {
                    if (strcmp(history[i].key, key) == 0) {
                        count++;
                    }
                }
            }

            printf("%lld\t%s\t%s\t%d\n", ts, key, ascii, count);
        }
    }
    return 0;
}
EOF

    gcc -O2 /tmp/oracle.c -o /app/oracle_tracker
    strip /app/oracle_tracker
    rm /tmp/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user