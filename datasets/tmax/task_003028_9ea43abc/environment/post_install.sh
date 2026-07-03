apt-get update && apt-get install -y python3 python3-pip gcc ffmpeg
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/oracle_calc.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_LINE 100000

int main() {
    char line[MAX_LINE];
    while (fgets(line, sizeof(line), stdin)) {
        int values[10000];
        int count = 0;
        char *token = strtok(line, " \t\n");
        while (token) {
            values[count++] = atoi(token);
            token = strtok(NULL, " \t\n");
        }
        if (count == 0 || count % 3 != 0) {
            continue;
        }
        for (int i = 0; i < (count / 3) - 1; i++) {
            int r1 = values[i*3];
            int g1 = values[i*3+1];
            int b1 = values[i*3+2];
            int r2 = values[i*3+3];
            int g2 = values[i*3+4];
            int b2 = values[i*3+5];
            double dist = sqrt(pow(r1 - r2, 2) + pow(g1 - g2, 2) + pow(b1 - b2, 2));
            printf("%d %d %d %d %d %d %d %d %.2f\n", i, i+1, r1, g1, b1, r2, g2, b2, dist);
        }
    }
    return 0;
}
EOF
    gcc -O3 /app/oracle_calc.c -o /app/oracle_calc -lm

    ffmpeg -f lavfi -i testsrc=duration=5:size=640x480:rate=1 -c:v libx264 /app/video.mp4 -y

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user