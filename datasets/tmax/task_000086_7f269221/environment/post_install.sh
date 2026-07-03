apt-get update && apt-get install -y python3 python3-pip gcc ffmpeg fonts-dejavu
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main() {
    char line[2048];
    while (fgets(line, sizeof(line), stdin)) {
        int len = strlen(line);
        int has_newline = 0;
        if (len > 0 && line[len-1] == '\n') {
            line[len-1] = '\0';
            has_newline = 1;
        }

        if (strcmp(line, "CRITICAL_ABORT!") == 0) {
            printf("--- SYSTEM HALTED ---\n");
            exit(0);
        }

        char *pos = strstr(line, "imagePullPolicy: Always");
        if (pos != NULL) {
            char buffer[4096];
            int prefix_len = pos - line;
            strncpy(buffer, line, prefix_len);
            buffer[prefix_len] = '\0';
            strcat(buffer, "imagePullPolicy: IfNotPresent");
            strcat(buffer, pos + strlen("imagePullPolicy: Always"));
            strcpy(line, buffer);
        }

        int i = 0;
        while (line[i] == ' ') i++;
        if (strncmp(line + i, "replicas:", 9) == 0) {
            int j = i + 9;
            while (line[j] == ' ') j++;
            int is_num = 1;
            int num_start = j;
            if (line[j] == '\0') is_num = 0;
            while (line[j] != '\0') {
                if (!isdigit(line[j])) { is_num = 0; break; }
                j++;
            }
            if (is_num) {
                int replicas = atoi(line + num_start);
                if (replicas > 5) {
                    line[i + 9] = ' ';
                    line[i + 10] = '5';
                    line[i + 11] = '\0';
                }
            }
        }

        printf("%s", line);
        if (has_newline) printf("\n");
    }
    return 0;
}
EOF

    gcc -o /app/oracle_filter /tmp/oracle.c
    chmod +x /app/oracle_filter

    ffmpeg -f lavfi -i color=c=black:s=320x240:d=2 -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:text='CRITICAL_ABORT!':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,1.1,1.3)'" -pix_fmt yuv420p /app/k8s_dashboard.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user