apt-get update && apt-get install -y python3 python3-pip gcc tesseract-ocr
pip3 install pytest Pillow

mkdir -p /app

# Create the image fixture using Python and Pillow
cat << 'EOF' > /app/make_img.py
from PIL import Image, ImageDraw

text = """PRIOR=0.5
P(D=1|H)=0.8
P(D=1|!H)=0.3
MISSING=-1
RESET=-2"""

# Create a simple image with the text
img = Image.new('RGB', (300, 150), color='white')
d = ImageDraw.Draw(img)
d.text((10, 10), text, fill='black')
img.save('/app/bayes_spec.png')
EOF

python3 /app/make_img.py
rm /app/make_img.py

# Create and compile the oracle
cat << 'EOF' > /app/oracle.c
#include <stdio.h>

int main() {
    double p_h = 0.5;
    int missing_mode = 0;
    int val;

    while (scanf("%d", &val) == 1) {
        if (val == -2) {
            p_h = 0.5;
            missing_mode = 0;
            printf("RESET\n");
            continue;
        }

        if (val == -1 || missing_mode) {
            missing_mode = 1;
            printf("NaN\n");
            continue;
        }

        if (val == 1) {
            p_h = (0.8 * p_h) / (0.8 * p_h + 0.3 * (1.0 - p_h));
        } else if (val == 0) {
            p_h = (0.2 * p_h) / (0.2 * p_h + 0.7 * (1.0 - p_h));
        }

        printf("%.4f\n", p_h);
    }
    return 0;
}
EOF

gcc -O3 /app/oracle.c -o /app/oracle
chmod +x /app/oracle

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user