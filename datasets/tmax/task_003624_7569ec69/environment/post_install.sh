apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install pytest

    mkdir -p /app

    # Generate telemetry feed video (5 seconds at 30 fps = 150 frames)
    ffmpeg -f lavfi -i testsrc=duration=5:rate=30 -c:v libx264 /app/telemetry_feed.mp4

    # Create oracle cleaner C program
    cat << 'EOF' > /app/oracle_cleaner.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RECORDS 150
#define MAX_DEVICES 1000

char seen_devices[MAX_DEVICES][65];
int seen_count = 0;

int is_seen(const char* dev) {
    for(int i=0; i<seen_count; i++) {
        if(strcmp(seen_devices[i], dev) == 0) return 1;
    }
    return 0;
}

void add_device(const char* dev) {
    if(seen_count < MAX_DEVICES) {
        strncpy(seen_devices[seen_count++], dev, 64);
    }
}

int main() {
    char line[2048];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    printf("%s", line); // header

    int records_printed = 0;
    int in_quotes = 0;
    char row_buffer[2048] = {0};
    int row_len = 0;
    int has_embedded_newline = 0;

    int c;
    while ((c = getchar()) != EOF) {
        if (c == '"') {
            in_quotes = !in_quotes;
        }
        if (c == '\n' && in_quotes) {
            has_embedded_newline = 1;
        }

        row_buffer[row_len++] = c;

        if (c == '\n' && !in_quotes) {
            row_buffer[row_len] = '\0';

            if (!has_embedded_newline) {
                // Parse CSV
                char ts[256]={0}, dev[256]={0}, ip[256]={0}, evt[1024]={0};
                // Simplified parsing for oracle based on assumptions
                int commas = 0;
                int idx = 0;
                for(int i=0; i<row_len; i++) {
                    if (row_buffer[i] == ',' && !in_quotes) {
                        commas++;
                        idx = 0;
                    } else if (commas == 0) ts[idx++] = row_buffer[i];
                    else if (commas == 1) dev[idx++] = row_buffer[i];
                    else if (commas == 2) ip[idx++] = row_buffer[i];
                    else if (commas == 3) evt[idx++] = row_buffer[i];
                }

                if (!is_seen(dev)) {
                    // Mask IP
                    char* last_dot = strrchr(ip, '.');
                    if (last_dot) {
                        *(last_dot + 1) = '\0';
                        strcat(ip, "XXX");
                    }

                    printf("%s,%s,%s,%s", ts, dev, ip, evt);
                    add_device(dev);
                    records_printed++;
                    if (records_printed >= MAX_RECORDS) {
                        break;
                    }
                }
            }

            row_len = 0;
            has_embedded_newline = 0;
            memset(row_buffer, 0, sizeof(row_buffer));
        }
    }
    return 0;
}
EOF

    gcc -o /app/oracle_cleaner /app/oracle_cleaner.c
    chmod +x /app/oracle_cleaner

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user