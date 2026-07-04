apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    mkdir -p /home/user/pipeline

    cat << 'EOF' > /home/user/pipeline/data.csv
1.0,2.0,5.0
2.0,4.0,4.0
3.0,6.0,3.0
4.0,8.0,2.0
5.0,10.0,1.0
EOF

    cat << 'EOF' > /home/user/pipeline/covar.c
#include <stdio.h>
#include <stdlib.h>

double data[1000][3];

void calc_cov(int n, int c1, int c2) {
    double sum1 = 0, sum2 = 0;
    double sum_prod; // BUG: uninitialized variable causing undefined/accumulated garbage behavior

    for(int i=0; i<n; i++) {
        sum1 += data[i][c1];
        sum2 += data[i][c2];
    }
    double mean1 = sum1/n;
    double mean2 = sum2/n;

    for(int i=0; i<n; i++) {
        sum_prod += (data[i][c1] - mean1) * (data[i][c2] - mean2);
    }
    printf("%.4f", sum_prod / (n - 1));
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <csv_file>\n", argv[0]);
        return 1;
    }
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    int n = 0;
    while (fscanf(f, "%lf,%lf,%lf", &data[n][0], &data[n][1], &data[n][2]) == 3) {
        n++;
    }
    fclose(f);

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            calc_cov(n, i, j);
            if (j < 2) printf(" ");
        }
        printf("\n");
    }
    return 0;
}
EOF

    chmod +x /home/user/pipeline/covar.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user