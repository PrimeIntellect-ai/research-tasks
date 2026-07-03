apt-get update && apt-get install -y python3 python3-pip gcc make wget unzip
    pip3 install pytest

    mkdir -p /app
    cd /app
    wget -q https://github.com/imneme/pcg-c/archive/refs/heads/master.zip
    unzip -q master.zip
    mv pcg-c-master pcg-c
    rm master.zip

    # Build pcg-c normally first to compile the oracle
    cd /app/pcg-c
    make

    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include "pcg_variants.h"

double kahan_mean(float* arr, int n) {
    double sum = 0.0;
    double c = 0.0;
    for (int i = 0; i < n; i++) {
        double y = (double)arr[i] - c;
        double t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    return sum / n;
}

int cmp(const void* a, const void* b) {
    double da = *(const double*)a;
    double db = *(const double*)b;
    return (da > db) - (da < db);
}

int main() {
    float *arr = malloc(1000000 * sizeof(float));
    int n = 0;
    while (fread(&arr[n], sizeof(float), 1, stdin) == 1) {
        n++;
    }
    if (n == 0) return 1;
    double orig_mean = kahan_mean(arr, n);
    pcg32_srandom(42u, 54u);
    double *boot_means = malloc(1000 * sizeof(double));
    float *boot_arr = malloc(n * sizeof(float));
    for (int i = 0; i < 1000; i++) {
        for (int j = 0; j < n; j++) {
            boot_arr[j] = arr[pcg32_boundedrand(n)];
        }
        boot_means[i] = kahan_mean(boot_arr, n);
    }
    qsort(boot_means, 1000, sizeof(double), cmp);
    printf("Original Mean: %.8f, 95%% CI: [%.8f, %.8f]\n", orig_mean, boot_means[24], boot_means[974]);
    return 0;
}
EOF

    gcc -O2 /opt/oracle/oracle.c -I/app/pcg-c/include -L/app/pcg-c/src -lpcg_random -o /opt/oracle/spectra_mean
    chmod +x /opt/oracle/spectra_mean

    # Clean pcg-c and apply perturbation
    cd /app/pcg-c
    make clean
    sed -i 's/-O2/O2/g' Makefile
    sed -i 's/-fPIC//g' Makefile

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user