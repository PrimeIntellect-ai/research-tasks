apt-get update && apt-get install -y python3 python3-pip g++ make
pip3 install pytest

mkdir -p /app/fast_bootstrap-1.0
cat << 'EOF' > /app/fast_bootstrap-1.0/bootstrap.h
#pragma once
void compute_ci(const float* data, int n, int seed, float& mean, float& lower, float& upper);
EOF

cat << 'EOF' > /app/fast_bootstrap-1.0/bootstrap.cpp
#include "bootstrap.h"
#include <vector>
#include <algorithm>
#include <random>

void compute_ci(const float* data, int n, int seed, float& mean, float& lower, float& upper) {
    std::mt19937 gen(seed);
    std::uniform_int_distribution<> dist(0, n - 1);
    const int num_bootstraps = 1000;
    std::vector<float> boot_means(num_bootstraps);

    float original_sum = 0.0f;
    for(int i=0; i<n; i++) original_sum += data[i];
    mean = original_sum / n;

    for (int b = 0; b < num_bootstraps; ++b) {
        float sum = 0.0f;
        // DELIBERATE PERTURBATION: non-deterministic FP reduction
        #pragma omp parallel for reduction(+:sum)
        for (int i = 0; i < n; ++i) {
            sum += data[dist(gen)];
        }
        boot_means[b] = sum / n;
    }
    std::sort(boot_means.begin(), boot_means.end());
    lower = boot_means[int(num_bootstraps * 0.025)];
    upper = boot_means[int(num_bootstraps * 0.975)];
}
EOF

cat << 'EOF' > /app/fast_bootstrap-1.0/Makefile
CX=g++
CFLAGS=-O3 -fopenmp

all: libfast_bootstrap.so

libfast_bootstrap.so: bootstrap.cpp
	$(CX) $(CFLAGS) -shared -o libfast_bootstrap.so bootstrap.cpp
EOF

mkdir -p /opt/oracle
# Compile the oracle with a fixed, sequential bootstrap.cpp
sed -i 's/#pragma omp parallel for reduction(+:sum)//' /app/fast_bootstrap-1.0/bootstrap.cpp
g++ -O3 -fPIC -shared -o /opt/oracle/libfast_bootstrap.so /app/fast_bootstrap-1.0/bootstrap.cpp

cat << 'EOF' > /opt/oracle/analyzer_oracle.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include "/app/fast_bootstrap-1.0/bootstrap.h"

int main(int argc, char** argv) {
    std::ifstream in(argv[1], std::ios::binary);
    std::ofstream out(argv[2], std::ios::binary);
    in.seekg(0, std::ios::end);
    size_t size = in.tellg();
    in.seekg(0, std::ios::beg);
    int num_floats = size / sizeof(float);
    int N = num_floats / 128;
    std::vector<float> data(num_floats);
    in.read((char*)data.data(), size);

    for (int i = 0; i < 128; ++i) {
        std::vector<float> bin_data(N);
        for (int j = 0; j < N; ++j) {
            bin_data[j] = data[j * 128 + i];
        }
        float mean, lower, upper;
        compute_ci(bin_data.data(), N, 42 + i, mean, lower, upper);
        float res[3] = {mean, lower, upper};
        out.write((char*)res, sizeof(res));
    }
    return 0;
}
EOF

g++ -O3 -o /opt/oracle/analyzer_oracle /opt/oracle/analyzer_oracle.cpp /opt/oracle/libfast_bootstrap.so -Wl,-rpath,/opt/oracle

# Reapply the perturbation
cat << 'EOF' > /app/fast_bootstrap-1.0/bootstrap.cpp
#include "bootstrap.h"
#include <vector>
#include <algorithm>
#include <random>

void compute_ci(const float* data, int n, int seed, float& mean, float& lower, float& upper) {
    std::mt19937 gen(seed);
    std::uniform_int_distribution<> dist(0, n - 1);
    const int num_bootstraps = 1000;
    std::vector<float> boot_means(num_bootstraps);

    float original_sum = 0.0f;
    for(int i=0; i<n; i++) original_sum += data[i];
    mean = original_sum / n;

    for (int b = 0; b < num_bootstraps; ++b) {
        float sum = 0.0f;
        #pragma omp parallel for reduction(+:sum)
        for (int i = 0; i < n; ++i) {
            sum += data[dist(gen)];
        }
        boot_means[b] = sum / n;
    }
    std::sort(boot_means.begin(), boot_means.end());
    lower = boot_means[int(num_bootstraps * 0.025)];
    upper = boot_means[int(num_bootstraps * 0.975)];
}
EOF

chmod -R 777 /app/fast_bootstrap-1.0

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user