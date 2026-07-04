apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
pip3 install pytest

mkdir -p /app/bin

# Generate video with black frames at specific indices
ffmpeg -f lavfi -i testsrc=duration=10:size=640x480:rate=30 -vf "drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill:enable='eq(n,42)+eq(n,43)+eq(n,89)+eq(n,144)+eq(n,145)+eq(n,146)+eq(n,250)'" -c:v libx264 -pix_fmt yuv420p /app/ui_walkthrough.mp4

# Create Oracle C program
cat << 'EOF' > /app/bin/oracle_process_loc.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int check_timestamp(const char *ts) {
    if (strlen(ts) != 20) return 0;
    if (ts[4] != '-' || ts[7] != '-' || ts[10] != 'T' || ts[13] != ':' || ts[16] != ':' || ts[19] != 'Z') return 0;
    for (int i=0; i<20; i++) {
        if (i==4||i==7||i==10||i==13||i==16||i==19) continue;
        if (!isdigit(ts[i])) return 0;
    }
    return 1;
}

int main() {
    char line[2048];
    int valid_count = 0;
    int dup_count = 0;
    char prev_key[1024] = {0};
    int has_prev = 0;

    while (fgets(line, sizeof(line), stdin)) {
        int len = strlen(line);
        if (len > 0 && line[len-1] == '\n') {
            line[len-1] = '\0';
            len--;
        }

        int pipes = 0;
        for(int i=0; i<len; i++) {
            if(line[i] == '|') pipes++;
        }
        if (pipes != 3) {
            printf("INVALID_RECORD\n");
            continue;
        }

        char ts[1024], email[1024], key[1024], text[1024];
        char *t1 = strchr(line, '|');
        if(!t1) { printf("INVALID_RECORD\n"); continue; }
        *t1 = '\0';
        strcpy(ts, line);

        char *t2 = strchr(t1+1, '|');
        if(!t2) { printf("INVALID_RECORD\n"); continue; }
        *t2 = '\0';
        strcpy(email, t1+1);

        char *t3 = strchr(t2+1, '|');
        if(!t3) { printf("INVALID_RECORD\n"); continue; }
        *t3 = '\0';
        strcpy(key, t2+1);
        strcpy(text, t3+1);

        if (!check_timestamp(ts)) {
            printf("INVALID_RECORD\n");
            continue;
        }

        if (has_prev && strcmp(key, prev_key) == 0) {
            dup_count++;
            continue;
        }

        char masked_email[1024];
        char *at = strchr(email, '@');
        if (at) {
            int local_len = at - email;
            if (local_len > 2) {
                sprintf(masked_email, "%c***%c%s", email[0], email[local_len-1], at);
            } else {
                strcpy(masked_email, email);
            }
        } else {
            strcpy(masked_email, email);
        }

        printf("%s|%s|%s|%s\n", ts, masked_email, key, text);
        strcpy(prev_key, key);
        has_prev = 1;
        valid_count++;
    }
    printf("STATS: Valid=[%d], Duplicates=[%d]\n", valid_count, dup_count);
    return 0;
}
EOF

gcc -O3 /app/bin/oracle_process_loc.c -o /app/bin/oracle_process_loc

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app