apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest

# Install task dependencies
apt-get install -y imagemagick tesseract-ocr libtesseract-dev gcc fonts-dejavu-core

# Create directories
mkdir -p /app
mkdir -p /home/user

# Create the image with the weights
convert -size 400x200 xc:white -font DejaVu-Sans -pointsize 24 -fill black \
    -draw "text 20,50 'Gap Filling Parameters:'" \
    -draw "text 20,90 'W1=0.2'" \
    -draw "text 20,120 'W2=0.3'" \
    -draw "text 20,150 'W3=0.5'" \
    -draw "text 20,180 'THRESHOLD=100.00'" \
    /app/weights.png

# Create the oracle program
cat << 'EOF' > /app/oracle_processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char line[256];
    float w1 = 0.2f, w2 = 0.3f, w3 = 0.5f;
    float threshold = 100.00f;
    float hist[3] = {0};
    int valid_count = 0;

    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\n")] = 0;
        if (strlen(line) == 0) continue;

        char *ts_str = strtok(line, ",");
        char *name = strtok(NULL, ",");
        char *val_str = strtok(NULL, ",");

        if (!ts_str || !name || !val_str) continue;

        float val = atof(val_str);

        for (int i = 0; name[i]; i++) {
            if (name[i] >= 'a' && name[i] <= 'z') {
                name[i] = name[i] - 32;
            }
        }

        if (val == -1.0f) {
            if (valid_count < 3) {
                val = threshold;
            } else {
                val = (w1 * hist[0]) + (w2 * hist[1]) + (w3 * hist[2]);
            }
        } else {
            hist[0] = hist[1];
            hist[1] = hist[2];
            hist[2] = val;
            valid_count++;
        }

        printf("%s,%s,%.2f\n", ts_str, name, val);
    }
    return 0;
}
EOF

gcc -O3 /app/oracle_processor.c -o /app/oracle_processor
chmod +x /app/oracle_processor

# Create user
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user