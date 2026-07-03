apt-get update && apt-get install -y python3 python3-pip gcc tesseract-ocr
    pip3 install pytest Pillow

    mkdir -p /app
    mkdir -p /home/user/logs
    mkdir -p /home/user/dumps
    mkdir -p /home/user/src

    # Generate requirement.png
    python3 -c "
from PIL import Image, ImageDraw
img = Image.new('RGB', (800, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = 'Hashing logic: For each character in the string, add its ASCII value multiplied by its 1-based index. Finally, XOR the total sum with 2023.'
d.text((10,10), text, fill=(0,0,0))
img.save('/app/requirement.png')
"

    # Create Logs
    cat << 'EOF' > /home/user/logs/service_api.log
[09:14:22] API request received.
[09:15:30] API request received.
EOF

    cat << 'EOF' > /home/user/logs/service_router.log
[09:14:23] Routing to hasher.
[09:15:31] Routing to hasher.
EOF

    cat << 'EOF' > /home/user/logs/hasher_service.log
[09:14:24] Processing started.
[09:14:25] SUCCESS.
[09:15:32] Processing started.
[09:15:33] FATAL FAULT: Segmentation violation.
EOF

    # Create Dumps
    dd if=/dev/urandom of=/home/user/dumps/dump_091425.bin bs=1K count=1 2>/dev/null
    echo -n -e "CRASH_STRING:old_report.txt\0" >> /home/user/dumps/dump_091425.bin
    dd if=/dev/urandom of=/home/user/dumps/dump_091533.bin bs=1K count=1 2>/dev/null
    echo -n -e "CRASH_STRING:quarterly report final version.pdf\0" >> /home/user/dumps/dump_091533.bin

    # Create buggy hasher.c
    cat << 'EOF' > /home/user/src/hasher.c
#include <stdio.h>
#include <string.h>

int main() {
    char buf[256];
    if (scanf("%s", buf) != 1) return 1;
    unsigned long sum = 0;
    for (size_t i = 0; i < strlen(buf); i++) {
        sum += (unsigned long)buf[i] * i;
    }
    sum = sum ^ 1000;
    printf("%lu\n", sum);
    return 0;
}
EOF

    # Create oracle_hasher.c
    cat << 'EOF' > /app/oracle_hasher.c
#include <stdio.h>
#include <string.h>

int main() {
    char buf[256];
    if (fgets(buf, sizeof(buf), stdin) == NULL) return 1;
    size_t len = strlen(buf);
    if (len > 0 && buf[len-1] == '\n') {
        buf[len-1] = '\0';
        len--;
    }
    unsigned long sum = 0;
    for (size_t i = 0; i < len; i++) {
        sum += (unsigned long)buf[i] * (i + 1);
    }
    sum = sum ^ 2023;
    printf("%lu\n", sum);
    return 0;
}
EOF
    gcc -o /app/oracle_hasher /app/oracle_hasher.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app