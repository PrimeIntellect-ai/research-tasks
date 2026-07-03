apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install pytest

    mkdir -p /app

    # Generate a 3-second, 30fps video (90 frames)
    ffmpeg -f lavfi -i testsrc=duration=3:size=320x240:rate=30 -c:v libx264 /app/experiment.mp4

    # Create and compile the oracle solver
    cat << 'EOF' > /app/oracle_solve.c
#include <stdio.h>

int main() {
    double A11, A12, A21, A22, b1, b2, lam;
    if (scanf("%lf %lf %lf %lf %lf %lf %lf", &A11, &A12, &A21, &A22, &b1, &b2, &lam) != 7) return 1;

    double M11 = A11*A11 + A21*A21 + lam;
    double M12 = A11*A12 + A21*A22;
    double M21 = M12;
    double M22 = A12*A12 + A22*A22 + lam;

    double y1 = A11*b1 + A21*b2;
    double y2 = A12*b1 + A22*b2;

    double det = M11*M22 - M12*M21;

    double x1 = (M22*y1 - M12*y2) / det;
    double x2 = (M11*y2 - M21*y1) / det;

    printf("%.6f %.6f\n", x1, x2);
    return 0;
}
EOF
    gcc /app/oracle_solve.c -o /app/oracle_solve
    chmod +x /app/oracle_solve

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user