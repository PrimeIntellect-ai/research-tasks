apt-get update && apt-get install -y python3 python3-pip git g++ make tcpdump
    pip3 install pytest scapy

    useradd -m -s /bin/bash user || true

    # Create working directories
    mkdir -p /home/user/sim_engine/src
    cd /home/user/sim_engine

    # Initialize Git
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    # Create initial stable code
    cat << 'EOF' > src/stats.cpp
#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>

double calculate_variance(const std::vector<float>& data) {
    if (data.empty()) return 0.0;
    double mean = 0.0;
    for (float x : data) mean += x;
    mean /= data.size();

    double variance = 0.0;
    for (float x : data) {
        variance += (x - mean) * (x - mean);
    }
    return variance / data.size();
}
EOF

    cat << 'EOF' > src/main.cpp
#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>

extern double calculate_variance(const std::vector<float>& data);

int main() {
    std::ifstream config("config.txt");
    if (!config) {
        std::cerr << "Missing config.txt\n";
        return 2;
    }
    double coeff;
    config >> coeff;

    // Generate data
    std::vector<float> data;
    for(int i=0; i<10000; ++i) {
        data.push_back(1000000.0f + (i % 10) * coeff);
    }

    double var = calculate_variance(data);
    if (std::isnan(var) || var < 0.0 || var > 1.0) {
        std::cerr << "Numerical instability detected! Variance: " << var << "\n";
        return 1;
    }
    std::cout << "Variance: " << var << " (Stable)\n";
    return 0;
}
EOF

    cat << 'EOF' > Makefile
CXX = g++
CXXFLAGS = -O2 -Wall -std=c++11

all: test_sim

test_sim: src/main.cpp src/stats.cpp
	$(CXX) $(CXXFLAGS) -o test_sim src/main.cpp src/stats.cpp

test: test_sim
	./test_sim

clean:
	rm -f test_sim
EOF

    cat << 'EOF' > .gitignore
config.txt
test_sim
EOF

    git add src/stats.cpp src/main.cpp Makefile .gitignore
    git commit -m "Initial commit"
    git tag v1.0

    # Add a few benign commits
    echo "// comment 1" >> src/main.cpp
    git commit -am "Add comment 1"

    echo "// comment 2" >> src/main.cpp
    git commit -am "Add comment 2"

    # Introduce the bad commit (numerical instability: catastrophic cancellation)
    cat << 'EOF' > src/stats.cpp
#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>

double calculate_variance(const std::vector<float>& data) {
    if (data.empty()) return 0.0;
    // Unstable one-pass formula
    float sum = 0.0f;
    float sum_sq = 0.0f;
    for (float x : data) {
        sum += x;
        sum_sq += x * x;
    }
    float mean = sum / data.size();
    return (sum_sq / data.size()) - (mean * mean);
}
EOF
    git commit -am "Optimize variance calculation to one-pass"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Add another benign commit
    echo "// comment 3" >> src/main.cpp
    git commit -am "Add comment 3"

    # Create the PCAP file using python and scapy
    cd /home/user
    cat << 'EOF' > generate_pcap.py
from scapy.all import *
packets = [
    IP(dst="192.168.1.100")/UDP(sport=1234, dport=5678)/Raw(load="STATUS=OK"),
    IP(dst="192.168.1.100")/UDP(sport=1234, dport=5678)/Raw(load="COEFF=0.0000015"),
    IP(dst="192.168.1.100")/UDP(sport=1234, dport=5678)/Raw(load="HEARTBEAT")
]
wrpcap("capture.pcap", packets)
EOF
    python3 generate_pcap.py
    rm generate_pcap.py

    # Save the expected truth to a hidden verification file
    cat << EOF > /home/user/.truth.txt
COEFFICIENT: 0.0000015
BAD_COMMIT: $BAD_COMMIT
BUG_FILE: src/stats.cpp
EOF

    chown -R user:user /home/user/sim_engine /home/user/capture.pcap /home/user/.truth.txt
    chmod -R 777 /home/user