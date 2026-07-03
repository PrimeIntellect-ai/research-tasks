apt-get update && apt-get install -y python3 python3-pip espeak gcc
    pip3 install pytest

    mkdir -p /app
    espeak -w /app/memo.wav "Please use five domains and four hundred bootstrap iterations."

    cat << 'EOF' > /app/oracle_analyze.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

uint32_t state = 1337;
uint32_t next_rand() {
    state = (state * 1103515245 + 12345) & 0x7FFFFFFF;
    return state;
}

int cmpfunc (const void * a, const void * b) {
   return ( *(int*)a - *(int*)b );
}

int main(int argc, char *argv[]) {
    if(argc != 2) return 1;
    char *seq = argv[1];
    int N = strlen(seq);
    int D = 5;
    int B = 400;

    int L_base = N / D;
    int widest_width = -1;
    int target_domain = -1;

    for(int d=0; d<D; d++) {
        int L = (d == D - 1) ? (N - d*L_base) : L_base;
        char *domain = seq + d*L_base;

        int counts[400];
        for(int b=0; b<B; b++) {
            int gc = 0;
            for(int i=0; i<L; i++) {
                int idx = next_rand() % L;
                char c = domain[idx];
                if(c == 'G' || c == 'C') gc++;
            }
            counts[b] = gc;
        }
        qsort(counts, B, sizeof(int), cmpfunc);
        int lower_idx = (int)(0.025 * B);
        int upper_idx = (int)(0.975 * B);
        int width = counts[upper_idx] - counts[lower_idx];

        if(width > widest_width) {
            widest_width = width;
            target_domain = d;
        }
    }
    printf("%d\n", target_domain);
    return 0;
}
EOF

    gcc -O3 -o /app/oracle_analyze /app/oracle_analyze.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user