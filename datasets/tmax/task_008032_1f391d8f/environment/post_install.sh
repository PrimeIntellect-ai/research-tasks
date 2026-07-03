apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/data

    cat << 'EOF' > /home/user/setup_data.py
import random

# Generate 1,000,000 random floating point numbers simulating spectroscopy data
random.seed(42)
data = [random.uniform(0.0001, 0.001) for _ in range(1000000)]

# Save to spectra.txt
with open('/home/user/data/spectra.txt', 'w') as f:
    for val in data:
        f.write(f"{val:.8f}\n")

# Calculate exact double precision sum for reference
total = sum(data)

# Save reference
with open('/home/user/reference.txt', 'w') as f:
    f.write(f"{total:.6f}\n")

EOF

    python3 /home/user/setup_data.py

    cat << 'EOF' > /home/user/spectroscopy_sim.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <omp.h>
#include <iomanip>

int main() {
    std::vector<float> spectra;
    std::ifstream infile("/home/user/data/spectra.txt");
    std::string line;

    while (std::getline(infile, line)) {
        spectra.push_back(std::stof(line));
    }

    float total_intensity = 0.0f;

    // BUG: Parallel reduction on float causes non-deterministic precision loss
    #pragma omp parallel for reduction(+:total_intensity)
    for (size_t i = 0; i < spectra.size(); ++i) {
        total_intensity += spectra[i];
    }

    std::cout << std::fixed << std::setprecision(6) << total_intensity << std::endl;

    return 0;
}
EOF

    chmod -R 777 /home/user