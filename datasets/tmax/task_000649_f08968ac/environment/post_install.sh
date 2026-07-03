apt-get update && apt-get install -y python3 python3-pip gcc libfftw3-dev
    pip3 install pytest numpy

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/dna_sim
    cd /home/user/dna_sim

    cat << 'EOF' > /tmp/setup_sim.py
import numpy as np

np.random.seed(42)
num_reads = 100
seq_length = 256

primer = "GATTACA"
bases = ['A', 'C', 'G', 'T']
mapping = {'A': 1.0, 'C': -1.0, 'G': 0.5, 'T': -0.5}

with open("/home/user/dna_sim/raw_reads.dat", "w") as f_raw, \
     open("/home/user/dna_sim/reference.txt", "w") as f_ref:

    seq_idx = 0
    for i in range(num_reads):
        # 40% chance to have the exact primer
        has_primer = np.random.rand() < 0.4

        if has_primer:
            seq = primer + "".join(np.random.choice(bases, seq_length - len(primer)))
        else:
            seq = "".join(np.random.choice(bases, seq_length))

        f_raw.write(f">Read_{i}\n{seq}\n")

        if has_primer:
            # Calculate exact deterministic reference
            signal = np.array([mapping[b] for b in seq], dtype=np.float64)
            fft_res = np.fft.fft(signal)
            energies = (fft_res.real**2 + fft_res.imag**2)
            energies_sorted = np.sort(energies)
            total_energy = np.sum(energies_sorted)
            f_ref.write(f"Sequence_{seq_idx}: {total_energy:.6f}\n")
            seq_idx += 1
EOF
    python3 /tmp/setup_sim.py

    cat << 'EOF' > /home/user/dna_sim/sim.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#include <fftw3.h>

#define MAX_SEQ_LEN 1024

double get_val(char c) {
    if (c == 'A') return 1.0;
    if (c == 'C') return -1.0;
    if (c == 'G') return 0.5;
    if (c == 'T') return -0.5;
    return 0.0;
}

int main() {
    FILE *f = fopen("filtered_reads.txt", "r");
    if (!f) {
        printf("Could not open filtered_reads.txt\n");
        return 1;
    }

    char line[MAX_SEQ_LEN + 2];
    int seq_idx = 0;

    while (fgets(line, sizeof(line), f)) {
        int len = strlen(line);
        if (line[len-1] == '\n') {
            line[len-1] = '\0';
            len--;
        }
        if (len == 0) continue;

        double *in = (double*) fftw_malloc(sizeof(double) * len);
        fftw_complex *out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * len);
        fftw_plan p = fftw_plan_dft_r2c_1d(len, in, out, FFTW_ESTIMATE);

        for (int i = 0; i < len; i++) {
            in[i] = get_val(line[i]);
        }

        fftw_execute(p);

        double total_energy = 0.0;

        // BUG: Non-deterministic reduction order
        #pragma omp parallel for reduction(+:total_energy)
        for (int i = 0; i < len; i++) {
            double real = out[i][0];
            double imag = out[i][1];
            total_energy += (real * real + imag * imag);
        }

        printf("Sequence_%d: %.6f\n", seq_idx, total_energy);

        fftw_destroy_plan(p);
        fftw_free(in);
        fftw_free(out);
        seq_idx++;
    }

    fclose(f);
    return 0;
}
EOF

    chmod -R 777 /home/user