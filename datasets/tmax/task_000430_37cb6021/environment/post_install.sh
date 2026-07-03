apt-get update && apt-get install -y python3 python3-pip gcc binutils
    pip3 install pytest numpy

    mkdir -p /app
    cat << 'EOF' > /tmp/spec_oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char** argv) {
    if (argc < 3) return 1;
    FILE* fin = fopen(argv[1], "r");
    if (!fin) return 1;
    int N, M;
    if (fscanf(fin, "%d %d", &N, &M) != 2) return 1;
    float** data = malloc(N * sizeof(float*));
    float** cdf = malloc(N * sizeof(float*));
    for(int i=0; i<N; i++) {
        data[i] = malloc(M * sizeof(float));
        cdf[i] = malloc(M * sizeof(float));
        float sum = 0;
        for(int j=0; j<M; j++) {
            fscanf(fin, "%f", &data[i][j]);
            sum += data[i][j];
            cdf[i][j] = sum;
        }
    }
    fclose(fin);

    FILE* fout = fopen(argv[2], "w");
    if (!fout) return 1;
    for(int i=0; i<N; i++) {
        for(int j=0; j<N; j++) {
            float dist = 0;
            for(int k=0; k<M; k++) {
                dist += fabs(cdf[i][k] - cdf[j][k]);
            }
            fprintf(fout, "%.6f ", dist);
        }
        fprintf(fout, "\n");
    }
    fclose(fout);
    return 0;
}
EOF

    gcc -O3 /tmp/spec_oracle.c -o /app/spec_oracle -lm
    strip /app/spec_oracle
    rm /tmp/spec_oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user