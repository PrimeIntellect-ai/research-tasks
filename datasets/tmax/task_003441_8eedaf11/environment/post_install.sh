apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest pillow

    mkdir -p /app/logs
    mkdir -p /home/user

    # Create oracle source and compile
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_ITER 500
#define TOLERANCE 0.000001

double f(double x) {
    return x * x * x - 2 * x - 5;
}

double df(double x) {
    return 3 * x * x - 2;
}

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;

    char *endptr;
    double x0 = strtod(argv[1], &endptr);

    int iter = 0;
    while (iter < MAX_ITER) {
        double fx = f(x0);
        double dfx = df(x0);
        if (fabs(fx) < TOLERANCE) {
            printf("%.6f\n", x0);
            return 0;
        }
        if (fabs(dfx) < 1e-12) {
            printf("CONVERGENCE_FAILURE\n");
            return 0;
        }
        x0 = x0 - fx / dfx;
        iter++;
    }
    printf("CONVERGENCE_FAILURE\n");
    return 0;
}
EOF
    gcc -O2 /app/oracle.c -o /app/oracle_solver -lm
    rm /app/oracle.c

    # Create flawed solver.c
    cat << 'EOF' > /home/user/solver.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define MAX_ITER 50
#define TOLERANCE 0.001

double f(double x) {
    return x * x * x - 2 * x - 5;
}

double df(double x) {
    return 3 * x * x - 2;
}

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;

    double x0;
    // Flawed parsing logic: fails on leading spaces
    if (argv[1][0] == ' ') {
        // Uninitialized x0 causes convergence failures
    } else {
        x0 = atof(argv[1]);
    }

    int iter = 0;
    while (iter < MAX_ITER) {
        double fx = f(x0);
        double dfx = df(x0);
        if (fabs(fx) < TOLERANCE) {
            printf("%.6f\n", x0);
            return 0;
        }
        if (fabs(dfx) < 1e-12) {
            printf("CONVERGENCE_FAILURE\n");
            return 0;
        }
        x0 = x0 - fx / dfx;
        iter++;
    }
    printf("CONVERGENCE_FAILURE\n");
    return 0;
}
EOF

    # Create core.dump
    python3 -c "
with open('/app/core.dump', 'wb') as f:
    f.write(b'\x00\x01\x02\x03\x04\x05' * 200)
    f.write(b'CRASH_INPUT: [    -4.52    ]')
    f.write(b'\x06\x07\x08\x09\x0A\x0B' * 200)
"

    # Create whiteboard.png
    python3 -c "
from PIL import Image, ImageDraw
img = Image.new('RGB', (400, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10, 10), 'Update parameters!\nMAX_ITER=500\nTOLERANCE=0.000001', fill=(0, 0, 0))
img.save('/app/whiteboard.png')
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app