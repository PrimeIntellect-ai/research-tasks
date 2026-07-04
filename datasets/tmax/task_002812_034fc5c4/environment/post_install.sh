apt-get update && apt-get install -y python3 python3-pip tesseract-ocr gcc
    pip3 install pytest Pillow

    mkdir -p /app

    # Create the watermark image using Python/Pillow
    cat << 'EOF' > /app/make_img.py
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (800, 100), color='white')
d = ImageDraw.Draw(img)
d.text((10, 40), "ConfigRecord[ID=%s, Rev=%s, Val=%s]", fill=(0,0,0))
img.save('/app/watermark.png')
EOF
    python3 /app/make_img.py
    rm /app/make_img.py

    # Create and compile the reference oracle
    cat << 'EOF' > /app/dedup_oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RECORDS 20000

typedef struct {
    int timestamp;
    char config_id[4];
    int revision;
    char value[33];
} Record;

Record records[MAX_RECORDS];
int num_records = 0;

int compare_records(const void *a, const void *b) {
    return strcmp(((Record*)a)->config_id, ((Record*)b)->config_id);
}

int main() {
    char line[256];
    Record current;
    while (fgets(line, sizeof(line), stdin)) {
        if (sscanf(line, "%d,%3[^,],%d,%32[^\n\r]", &current.timestamp, current.config_id, &current.revision, current.value) == 4) {
            int found = 0;
            for (int i = 0; i < num_records; i++) {
                if (strcmp(records[i].config_id, current.config_id) == 0) {
                    found = 1;
                    if (current.timestamp > records[i].timestamp) {
                        records[i] = current;
                    }
                    break;
                }
            }
            if (!found && num_records < MAX_RECORDS) {
                records[num_records++] = current;
            }
        }
    }

    qsort(records, num_records, sizeof(Record), compare_records);

    for (int i = 0; i < num_records; i++) {
        printf("ConfigRecord[ID=%s, Rev=%d, Val=%s]\n", records[i].config_id, records[i].revision, records[i].value);
    }
    return 0;
}
EOF
    gcc -O3 /app/dedup_oracle.c -o /app/dedup_oracle
    strip /app/dedup_oracle
    rm /app/dedup_oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user