apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest numpy

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/generate_data.py
import numpy as np
np.random.seed(42)
data = np.random.normal(loc=5.0, scale=1.0, size=100000)
data = np.sort(data)[::-1]
with open('/home/user/dataset.txt', 'w') as f:
    for x in data:
        f.write(f"{x:.8f}\n")
EOF

    python3 /home/user/generate_data.py

    cat << 'EOF' > /home/user/sampler_kahan.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <cmath>
#include <iomanip>

double log_likelihood(double mu, const std::vector<double>& data) {
    double sum = 0.0;
    double c = 0.0;
    for (double x : data) {
        double y = -0.5 * (x - mu) * (x - mu) - c;
        double t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    return sum;
}

int main() {
    std::vector<double> data;
    std::ifstream infile("/home/user/dataset.txt");
    double val;
    while (infile >> val) {
        data.push_back(val);
    }

    std::mt19937 gen(12345);
    std::normal_distribution<double> proposal(0.0, 0.05);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);

    double current_mu = 0.0;
    double current_ll = log_likelihood(current_mu, data);

    std::ofstream outfile("/home/user/reference_chain.csv");
    outfile << std::fixed << std::setprecision(8);

    for (int i = 0; i < 500; ++i) {
        double proposed_mu = current_mu + proposal(gen);
        double proposed_ll = log_likelihood(proposed_mu, data);

        double log_accept_ratio = proposed_ll - current_ll;
        if (std::log(uniform(gen)) < log_accept_ratio) {
            current_mu = proposed_mu;
            current_ll = proposed_ll;
        }
        outfile << current_mu << "\n";
    }
    return 0;
}
EOF

    cd /home/user
    g++ -O3 -std=c++11 sampler_kahan.cpp -o sampler_ref
    ./sampler_ref
    rm sampler_ref sampler_kahan.cpp generate_data.py

    cat << 'EOF' > /home/user/sampler.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <cmath>
#include <iomanip>

double log_likelihood(double mu, const std::vector<double>& data) {
    double sum = 0.0;
    for (double x : data) {
        sum += -0.5 * (x - mu) * (x - mu);
    }
    return sum;
}

int main() {
    std::vector<double> data;
    std::ifstream infile("/home/user/dataset.txt");
    double val;
    while (infile >> val) {
        data.push_back(val);
    }

    std::mt19937 gen(12345);
    std::normal_distribution<double> proposal(0.0, 0.05);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);

    double current_mu = 0.0;
    double current_ll = log_likelihood(current_mu, data);

    std::ofstream outfile("chain.csv");
    outfile << std::fixed << std::setprecision(8);

    for (int i = 0; i < 500; ++i) {
        double proposed_mu = current_mu + proposal(gen);
        double proposed_ll = log_likelihood(proposed_mu, data);

        double log_accept_ratio = proposed_ll - current_ll;
        if (std::log(uniform(gen)) < log_accept_ratio) {
            current_mu = proposed_mu;
            current_ll = proposed_ll;
        }
        outfile << current_mu << "\n";
    }
    return 0;
}
EOF

    chmod -R 777 /home/user