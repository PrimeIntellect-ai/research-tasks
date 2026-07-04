apt-get update && apt-get install -y python3 python3-pip gcc imagemagick
    pip3 install pytest

    mkdir -p /app

    # Create oracle source code
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 256

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    double x[N], y[N];
    if (fread(x, sizeof(double), N, f) != N) return 1;
    if (fread(y, sizeof(double), N, f) != N) return 1;
    fclose(f);

    double D = 0.0;
    for (int k = 0; k < N; k++) {
        double X_re = 0.0, X_im = 0.0;
        double Y_re = 0.0, Y_im = 0.0;
        for (int n = 0; n < N; n++) {
            double angle = -2.0 * M_PI * k * n / N;
            double c = cos(angle);
            double s = sin(angle);
            X_re += x[n] * c;
            X_im += x[n] * s;
            Y_re += y[n] * c;
            Y_im += y[n] * s;
        }
        double mag_X = sqrt(X_re * X_re + X_im * X_im);
        double mag_Y = sqrt(Y_re * Y_re + Y_im * Y_im);
        double diff = mag_X - mag_Y;
        D += (diff * diff) / (k + 1.0);
    }
    printf("%.15e\n", D);
    return 0;
}
EOF

    # Compile the oracle
    gcc -O3 /app/oracle.c -o /app/oracle_bin -lm
    rm /app/oracle.c

    # Generate the image
    convert -background white -fill black -pointsize 18 label:"Calculate D:\nX = NaiveDFT(x)\nY = NaiveDFT(y)\nD = sum_{k=0}^{N-1} (sqrt(Re(X[k])^2 + Im(X[k])^2) - sqrt(Re(Y[k])^2 + Im(Y[k])^2))^2 / (k + 1.0)\nWhere NaiveDFT(s)[k] = sum_{n=0}^{N-1} s[n] * (cos(-2*pi*k*n/N) + i*sin(-2*pi*k*n/N))" /app/equation_def.png

    chmod 755 /app/oracle_bin
    chmod 644 /app/equation_def.png

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user