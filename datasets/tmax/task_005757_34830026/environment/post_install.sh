apt-get update && apt-get install -y python3 python3-pip gcc golang wget
    pip3 install pytest numpy scipy

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/src /home/user/bin /home/user/data /home/user/analyze

    cat << 'EOF' > /home/user/src/kmer_counter.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int kmer_to_idx(const char* kmer) {
    int idx = 0;
    for(int i=0; i<3; i++) {
        idx <<= 2;
        switch(kmer[i]) {
            case 'A': break;
            case 'C': idx |= 1; break;
            case 'G': idx |= 2; break;
            case 'T': idx |= 3; break;
            default: return -1;
        }
    }
    return idx;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    FILE* f = fopen(argv[1], "r");
    if (!f) return 1;

    char line[1024];
    int counts[64] = {0};
    int in_seq = 0;
    char seq[10000] = {0};
    int seq_len = 0;

    while (fgets(line, sizeof(line), f)) {
        if (line[0] == '>') {
            if (seq_len > 0) {
                memset(counts, 0, sizeof(counts));
                for(int i=0; i<=seq_len-3; i++) {
                    int idx = kmer_to_idx(seq + i);
                    if(idx >= 0) counts[idx]++;
                }
                for(int i=0; i<64; i++) {
                    printf("%d%s", counts[i], (i==63)?"\n":",");
                }
            }
            seq_len = 0;
            in_seq = 1;
        } else if (in_seq) {
            for(int i=0; line[i] != '\0'; i++) {
                if (line[i] == 'A' || line[i] == 'C' || line[i] == 'G' || line[i] == 'T') {
                    seq[seq_len++] = line[i];
                }
            }
        }
    }
    if (seq_len > 0) {
        memset(counts, 0, sizeof(counts));
        for(int i=0; i<=seq_len-3; i++) {
            int idx = kmer_to_idx(seq + i);
            if(idx >= 0) counts[idx]++;
        }
        for(int i=0; i<64; i++) {
            printf("%d%s", counts[i], (i==63)?"\n":",");
        }
    }
    fclose(f);
    return 0;
}
EOF

    cat << 'EOF' > /tmp/gen_fasta.py
import random

random.seed(42)
bases = ['A', 'C', 'G', 'T']
with open('/home/user/data/seqs.fasta', 'w') as f:
    for i in range(100):
        f.write(f">seq_{i}\n")
        seq = []
        for j in range(500):
            if random.random() < 0.1:
                seq.append(random.choice(['G', 'C']))
            else:
                seq.append(random.choice(bases))
        f.write("".join(seq) + "\n")
EOF
    python3 /tmp/gen_fasta.py

    gcc -O3 /home/user/src/kmer_counter.c -o /home/user/bin/kmer_counter
    /home/user/bin/kmer_counter /home/user/data/seqs.fasta > /home/user/data/matrix.csv

    cat << 'EOF' > /tmp/calc_truth.py
import numpy as np
from scipy.linalg import svd
import json

data = np.loadtxt('/home/user/data/matrix.csv', delimiter=',')
U, S, Vh = svd(data, full_matrices=False)
cond = S[0] / S[-1]

y = np.log(S)
x = np.arange(len(S))

A_mat = np.vstack([x, np.ones(len(x))]).T
m, c = np.linalg.lstsq(A_mat, y, rcond=None)[0]

b = -m
A = np.exp(c)

print(json.dumps({"condition_number": cond, "A": A, "b": b}))
EOF
    python3 /tmp/calc_truth.py > /home/user/truth.json

    rm /home/user/bin/kmer_counter /home/user/data/matrix.csv

    chown -R user:user /home/user
    chmod -R 777 /home/user