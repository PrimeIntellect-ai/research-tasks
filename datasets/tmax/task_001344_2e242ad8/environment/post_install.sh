apt-get update && apt-get install -y python3 python3-pip golang-go gcc libc-dev
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/feature_projector.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {
    float f[20];
    float sum = 0;
    float sq_sum = 0;

    for (int i = 0; i < 20; i++) {
        if (i < 19) {
            if (scanf("%f,", &f[i]) != 1) return 1;
        } else {
            if (scanf("%f", &f[i]) != 1) return 1;
        }
        sum += f[i];
        sq_sum += f[i] * f[i];
    }

    float norm = sqrt(sq_sum);

    if (sum < 0.0 || norm > 50.0) {
        printf("NaN\n");
        return 1;
    }

    printf("%f,%f,%f,%f,%f\n", f[0]*0.5, f[1]*0.5, f[2]*0.5, f[3]*0.5, f[4]*0.5);
    return 0;
}
EOF
    gcc -O2 /app/feature_projector.c -lm -o /app/feature_projector
    strip /app/feature_projector
    rm /app/feature_projector.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user