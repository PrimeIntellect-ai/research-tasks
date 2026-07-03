apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install pytest

    mkdir -p /app

    # Generate the video fixture
    ffmpeg -f lavfi -i testsrc=duration=10:size=320x240:rate=10 -c:v libx264 /app/experiment_video.mp4

    # Create the oracle program
    cat << 'EOF' > /app/oracle_fast_query.c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    double pts_time;
    int size;
} Frame;

int main() {
    FILE *fp = popen("ffprobe -v error -select_streams v:0 -show_entries packet=pts_time,size -of csv=p=0 /app/experiment_video.mp4", "r");
    if (!fp) return 1;

    Frame frames[1000];
    int count = 0;
    while (fscanf(fp, "%lf,%d", &frames[count].pts_time, &frames[count].size) == 2) {
        count++;
    }
    pclose(fp);

    double t;
    while (scanf("%lf", &t) == 1) {
        if (count == 0 || t < frames[0].pts_time) {
            printf("%.4f -> NaN\n", t);
        } else {
            int left = 0, right = count - 1;
            int best = 0;
            while (left <= right) {
                int mid = left + (right - left) / 2;
                if (frames[mid].pts_time <= t) {
                    best = mid;
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
            printf("%.4f -> %d\n", t, frames[best].size);
        }
        fflush(stdout);
    }
    return 0;
}
EOF

    gcc -O3 /app/oracle_fast_query.c -o /app/oracle_fast_query

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user