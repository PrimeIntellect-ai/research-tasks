apt-get update && apt-get install -y python3 python3-pip build-essential
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/compute_spectrum.cpp
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <omp.h>

using namespace std;

void compute_power_spectrum(const string& seq, vector<float>& power) {
    int N = seq.length();
    power.assign(N, 0.0f);
    for(int k=0; k<N; ++k) {
        float real_part = 0.0f;
        float imag_part = 0.0f;
        for(int n=0; n<N; ++n) {
            float val = (seq[n] == 'A' || seq[n] == 'G') ? 1.0f : -1.0f; 
            float angle = -2.0f * M_PI * k * n / N;
            real_part += val * cos(angle);
            imag_part += val * sin(angle);
        }
        power[k] = (real_part*real_part + imag_part*imag_part);
    }
}

int main() {
    vector<string> seqs;
    ifstream in("/home/user/sequences.txt");
    string line;
    while(in >> line) seqs.push_back(line);

    int num_seqs = seqs.size();
    if(num_seqs == 0) return 0;
    int N = seqs[0].length();

    vector<float> avg_power(N, 0.0f);

    #pragma omp parallel for
    for(int i=0; i<num_seqs; ++i) {
        vector<float> power;
        compute_power_spectrum(seqs[i], power);
        for(int k=0; k<N; ++k) {
            #pragma omp atomic
            avg_power[k] += power[k] / num_seqs;
        }
    }

    ofstream out("/home/user/avg_spectrum.txt");
    for(int k=0; k<N; ++k) {
        out << avg_power[k] << endl;
    }
    return 0;
}
EOF

    cat << 'EOF' > /home/user/generate_data.py
import random
import math

random.seed(42)
with open("/home/user/sequences.txt", "w") as f:
    for _ in range(100):
        f.write("".join(random.choices(['A', 'C', 'G', 'T'], k=64)) + "\n")

with open("/home/user/sequences.txt", "r") as f:
    seqs = [line.strip() for line in f if line.strip()]

N = len(seqs[0])
avg_power = [0.0] * N

for seq in seqs:
    for k in range(N):
        real_part = 0.0
        imag_part = 0.0
        for n in range(N):
            val = 1.0 if seq[n] in ('A', 'G') else -1.0
            angle = -2.0 * math.pi * k * n / N
            real_part += val * math.cos(angle)
            imag_part += val * math.sin(angle)
        avg_power[k] += (real_part*real_part + imag_part*imag_part) / len(seqs)

with open("/home/user/reference_spectrum.txt", "w") as f:
    for val in avg_power:
        f.write(f"{val}\n")
EOF

    python3 /home/user/generate_data.py
    rm /home/user/generate_data.py

    chmod -R 777 /home/user