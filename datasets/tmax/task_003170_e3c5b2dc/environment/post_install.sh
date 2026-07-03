apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest pillow

    mkdir -p /app

    # Generate the pipeline image
    cat << 'EOF' > /tmp/gen_image.py
from PIL import Image, ImageDraw

text = """PIPELINE STAGES:
1. FILTER: status == "active"
2. SORT: score DESCENDING. If tied, sort by id ASCENDING.
3. LIMIT: N (from standard input)"""

img = Image.new('RGB', (600, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((20, 20), text, fill=(0, 0, 0))
img.save('/app/pipeline.png')
EOF
    python3 /tmp/gen_image.py
    rm /tmp/gen_image.py

    # Create and compile the oracle executable
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int id;
    char status[24];
    int age;
    int score;
} Record;

int cmp(const void *a, const void *b) {
    Record *ra = (Record *)a;
    Record *rb = (Record *)b;
    if (ra->score != rb->score) {
        return rb->score - ra->score; // DESC
    }
    return ra->id - rb->id; // ASC
}

int main() {
    int limit;
    if (scanf("%d\n", &limit) != 1) return 0;

    Record *records = malloc(50000 * sizeof(Record));
    int count = 0;
    char line[256];

    while (fgets(line, sizeof(line), stdin)) {
        int id, age, score;
        char status[24];
        if (sscanf(line, "%d,%23[^,],%d,%d", &id, status, &age, &score) == 4) {
            if (strcmp(status, "active") == 0) {
                records[count].id = id;
                strcpy(records[count].status, status);
                records[count].age = age;
                records[count].score = score;
                count++;
            }
        }
    }

    qsort(records, count, sizeof(Record), cmp);

    int out_count = limit < count ? limit : count;
    for (int i = 0; i < out_count; i++) {
        printf("{\"id\": %d, \"score\": %d}\n", records[i].id, records[i].score);
    }

    free(records);
    return 0;
}
EOF
    gcc -O3 /app/oracle.c -o /app/oracle_exec
    chmod +x /app/oracle_exec

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user