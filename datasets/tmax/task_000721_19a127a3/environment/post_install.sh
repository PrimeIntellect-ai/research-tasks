apt-get update && apt-get install -y python3 python3-pip gcc build-essential
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/gen_oracle.c
#include <stdio.h>
#include <stdlib.h>

void solve(double alpha, double beta, double gamma, double delta) {
    double x = 2.0;
    double y = 1.0;
    double x_arr[501];
    for (int k = 0; k <= 500; k++) {
        x_arr[k] = x;
        double dx = alpha * x - beta * x * y;
        double dy = delta * x * y - gamma * y;
        x += 0.01 * dx;
        y += 0.01 * dy;
    }

    double MtM[3][3] = {0};
    double MtX[3] = {0};

    for (int k = 0; k <= 500; k++) {
        double t_k = k * 0.01;
        double row[3] = {1.0, t_k, t_k * t_k};
        for (int i = 0; i < 3; i++) {
            MtX[i] += row[i] * x_arr[k];
            for (int j = 0; j < 3; j++) {
                MtM[i][j] += row[i] * row[j];
            }
        }
    }

    MtM[0][0] += 0.0001;
    MtM[1][1] += 0.0001;
    MtM[2][2] += 0.0001;

    double det = MtM[0][0]*(MtM[1][1]*MtM[2][2] - MtM[1][2]*MtM[2][1])
               - MtM[0][1]*(MtM[1][0]*MtM[2][2] - MtM[1][2]*MtM[2][0])
               + MtM[0][2]*(MtM[1][0]*MtM[2][1] - MtM[1][1]*MtM[2][0]);

    double det0 = MtX[0]*(MtM[1][1]*MtM[2][2] - MtM[1][2]*MtM[2][1])
                - MtM[0][1]*(MtX[1]*MtM[2][2] - MtM[1][2]*MtX[2])
                + MtM[0][2]*(MtX[1]*MtM[2][1] - MtM[1][1]*MtX[2]);

    double det1 = MtM[0][0]*(MtX[1]*MtM[2][2] - MtM[1][2]*MtX[2])
                - MtX[0]*(MtM[1][0]*MtM[2][2] - MtM[1][2]*MtM[2][0])
                + MtM[0][2]*(MtM[1][0]*MtX[2] - MtX[1]*MtM[2][0]);

    double det2 = MtM[0][0]*(MtM[1][1]*MtX[2] - MtX[1]*MtM[2][1])
                - MtM[0][1]*(MtM[1][0]*MtX[2] - MtX[1]*MtM[2][0])
                + MtX[0]*(MtM[1][0]*MtM[2][1] - MtM[1][1]*MtM[2][0]);

    printf("%.6f %.6f %.6f\n", det0/det, det1/det, det2/det);
}

int main() {
    int N;
    if (scanf("%d", &N) != 1) return 1;
    for (int i = 0; i < N; i++) {
        double a, b, c, d;
        if (scanf("%lf %lf %lf %lf", &a, &b, &c, &d) != 4) return 1;
        solve(a, b, c, d);
    }
    return 0;
}
EOF

    gcc -O3 -o /app/gen_oracle /app/gen_oracle.c
    strip /app/gen_oracle
    rm /app/gen_oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user