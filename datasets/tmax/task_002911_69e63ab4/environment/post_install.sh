apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick gcc
    pip3 install pytest

    mkdir -p /app

    # Create image
    convert -size 100x50 xc:white -fill black -pointsize 36 -gravity center -annotate +0+0 "4" /app/config.png

    # Oracle C code
    cat << 'EOF' > /app/oracle_truncate_lu.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    double A[10][10], L[10][10] = {0}, U[10][10] = {0}, A_prime[10][10] = {0};
    if (fread(A, sizeof(double), 100, stdin) != 100) return 1;

    int k = 4; // Ground truth from image
    int n = 10;

    // LU Decomposition
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            double sum = 0;
            for (int p = 0; p < i; p++) sum += (L[i][p] * U[p][j]);
            U[i][j] = A[i][j] - sum;
        }
        for (int j = i; j < n; j++) {
            if (i == j) L[i][i] = 1;
            else {
                double sum = 0;
                for (int p = 0; p < i; p++) sum += (L[j][p] * U[p][i]);
                L[j][i] = (A[j][i] - sum) / U[i][i];
            }
        }
    }

    // Truncated multiplication
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0;
            for (int p = 0; p < k; p++) {
                sum += L[i][p] * U[p][j];
            }
            A_prime[i][j] = sum;
        }
    }

    fwrite(A_prime, sizeof(double), 100, stdout);
    return 0;
}
EOF

    gcc -O3 /app/oracle_truncate_lu.c -o /app/oracle_truncate_lu

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user