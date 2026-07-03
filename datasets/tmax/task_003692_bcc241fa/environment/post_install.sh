apt-get update && apt-get install -y python3 python3-pip git gcc tesseract-ocr
    pip3 install pytest Pillow

    mkdir -p /app

    # Generate image artifact
    python3 -c "
from PIL import Image, ImageDraw
img = Image.new('RGB', (400, 100), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10,50), 'COEFFICIENT=7.482', fill=(0,0,0))
img.save('/app/matrix_coef.png')
"

    # Create oracle solver
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    float mat[16];
    for (int i = 0; i < 16; i++) {
        if (scanf("%f", &mat[i]) != 1) return 1;
    }
    float coef = 7.482;
    for (int i = 0; i < 16; i++) {
        printf("%.4f ", mat[i] * coef);
    }
    printf("\n");
    return 0;
}
EOF
    gcc /app/oracle.c -o /app/oracle_solver
    chmod +x /app/oracle_solver

    # Set up git repository
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/math_solver/src
    cd /home/user/math_solver
    git init
    git config user.email "dev@example.com"
    git config user.name "Dev"

    cat << 'EOF' > src/transform.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    float mat[16];
    for (int i = 0; i < 16; i++) {
        if (scanf("%f", &mat[i]) != 1) return 1;
    }
    float coef = 7.482;
    for (int i = 0; i < 16; i++) {
        printf("%.4f ", mat[i] * coef);
    }
    printf("\n");
    return 0;
}
EOF

    cat << 'EOF' > Makefile
all:
	mkdir -p bin
	gcc src/transform.c -o bin/solver
EOF

    git add src/transform.c Makefile
    git commit -m "Initial commit"

    for i in $(seq 2 155); do
        echo "// Dummy comment $i" >> src/transform.c
        git commit -am "Commit $i"
    done

    # Introduce bug at HEAD~45 (commit 156 of 200)
    sed -i 's/float coef = 7.482;/float coef = 7.400;/' src/transform.c
    git commit -am "Optimize fast-path coefficient"

    for i in $(seq 157 200); do
        echo "// Dummy comment $i" >> src/transform.c
        git commit -am "Commit $i"
    done

    chmod -R 777 /home/user
    chmod -R 777 /app