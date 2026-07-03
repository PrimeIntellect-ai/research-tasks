apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc tzdata
pip3 install pytest numpy opencv-python-headless

mkdir -p /app
mkdir -p /home/user
mkdir -p /var/log

cat << 'EOF' > /app/generate_video.py
import cv2
import numpy as np
out = cv2.VideoWriter('/app/iot_feed.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
for i in range(150):
    if i in [23, 89, 142]:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
    else:
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    out.write(frame)
out.release()
EOF

python3 /app/generate_video.py

cat << 'EOF' > /app/oracle_processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main() {
    char *device_id = getenv("DEVICE_ID");
    if (!device_id) device_id = "UNKNOWN";

    tzset();

    int threshold = 80;
    char admin_email[256] = "admin@iot.local";

    FILE *conf = fopen("/home/user/edge.conf", "r");
    if (conf) {
        char line[256];
        while (fgets(line, sizeof(line), conf)) {
            if (strncmp(line, "THRESHOLD=", 10) == 0) threshold = atoi(line + 10);
            else if (strncmp(line, "ADMIN_EMAIL=", 12) == 0) {
                strcpy(admin_email, line + 12);
                admin_email[strcspn(admin_email, "\r\n")] = 0;
            }
        }
        fclose(conf);
    }

    long ts;
    int val;
    while (scanf("%ld %d", &ts, &val) == 2) {
        time_t t = ts;
        struct tm *tm_info = localtime(&t);
        char buffer[26];
        strftime(buffer, 26, "%Y-%m-%d %H:%M:%S", tm_info);

        if (val >= threshold) {
            printf("[%s] %s - ALERT: %d >= %d. Emailing %s\n", device_id, buffer, val, threshold, admin_email);
        } else {
            printf("[%s] %s - OK: %d\n", device_id, buffer, val);
        }
    }
    return 0;
}
EOF

gcc /app/oracle_processor.c -o /app/oracle_processor

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app
chmod -R 777 /var/log