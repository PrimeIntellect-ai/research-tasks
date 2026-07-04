apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    apt-get install -y python3-h5py python3-numpy build-essential libhdf5-dev

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/generate_h5.py
import h5py
import numpy as np

np.random.seed(123)
initial_conditions = np.random.uniform(1.0, 10.0, 1000).astype(np.float64)

with h5py.File('/home/user/init_cond.h5', 'w') as f:
    f.create_dataset('ic', data=initial_conditions)
EOF
    python3 /home/user/generate_h5.py

    cat << 'EOF' > /home/user/mc_ode_sim.cpp
#include <iostream>
#include <vector>
#include <random>
#include <cmath>
#include <omp.h>
#include <H5Cpp.h>
#include <fstream>
#include <iomanip>
#include <algorithm>

using namespace H5;

int main() {
    // Read from HDF5
    H5File file("/home/user/init_cond.h5", H5F_ACC_RDONLY);
    DataSet dataset = file.openDataSet("ic");
    DataSpace dataspace = dataset.getSpace();
    hsize_t dims[1];
    dataspace.getSimpleExtentDims(dims, NULL);
    int N = dims[0];

    std::vector<double> ic(N);
    dataset.read(ic.data(), PredType::NATIVE_DOUBLE);

    double dt = 0.01;
    int steps = 100;

    double total_sum = 0.0;

    #pragma omp parallel for
    for (int i = 0; i < N; ++i) {
        // Thread-local RNG seeded by path index for reproducible paths
        std::mt19937 gen(1000 + i);
        std::normal_distribution<double> dist(0.0, 1.0);

        double y = ic[i];
        for (int step = 0; step < steps; ++step) {
            double dW = dist(gen) * std::sqrt(dt);
            y += -0.5 * y * dt + 0.1 * y * dW; // Geometric Brownian Motion drift
        }

        #pragma omp atomic
        total_sum += y;
    }

    std::cout << "Sum: " << total_sum << std::endl;
    return 0;
}
EOF

    chmod -R 777 /home/user