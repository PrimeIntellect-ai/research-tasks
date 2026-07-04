apt-get update && apt-get install -y python3 python3-pip g++ bc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/mcmc_sampler.cpp
#include <iostream>
#include <cmath>
#include <random>
#include <fstream>

double target_pdf(double x) {
    double mu = 5.0;
    double sigma = 2.0;
    return std::exp(-0.5 * std::pow((x - mu) / sigma, 2)) / (sigma * std::sqrt(2.0 * M_PI));
}

int main() {
    std::mt19937 gen(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);

    double current = 0.0;
    double delta = 10000.0; // BUG: Proposal step size is astronomically large
    std::normal_distribution<double> proposal(0.0, delta);

    int num_samples = 100000;
    int burn_in = 10000;
    double sum = 0.0;
    int accepted = 0;

    for (int i = 0; i < num_samples + burn_in; ++i) {
        // Re-initialize distribution in case delta was changed in code
        std::normal_distribution<double> current_proposal(0.0, delta);
        double proposed = current + current_proposal(gen);

        // BUG: Incorrect acceptance ratio (flipped)
        double alpha = target_pdf(current) / target_pdf(proposed); 

        if (uniform(gen) < alpha) {
            current = proposed;
            if (i >= burn_in) accepted++;
        }

        if (i >= burn_in) {
            sum += current;
        }
    }

    double mean = sum / num_samples;
    std::cout << "Mean: " << mean << std::endl;
    std::cout << "Acceptance rate: " << (double)accepted / num_samples << std::endl;

    return 0;
}
EOF

    chmod -R 777 /home/user