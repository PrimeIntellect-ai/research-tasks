apt-get update && apt-get install -y python3 python3-pip git g++ make gdb
    pip3 install pytest

    mkdir -p /home/user/uptime_monitor
    cd /home/user/uptime_monitor

    git config --global user.email "sre@example.com"
    git config --global user.name "SRE"
    git init

    cat << 'EOF' > Makefile
all: monitor
monitor: main.cpp
	g++ -g -O0 main.cpp -o monitor
clean:
	rm -f monitor
EOF

    cat << 'EOF' > main.cpp
#include <iostream>
#include <vector>
#include <fstream>

double calculate_weighted_average(const std::vector<int>& values, const std::vector<int>& weights) {
    double sum = 0;
    double weight_sum = 0;
    for (size_t i = 0; i < values.size(); ++i) {
        sum += values[i] * weights[i];
        weight_sum += weights[i];
    }
    return sum / weight_sum;
}

int main() {
    std::vector<int> vals = {100, 200, 150};
    std::vector<int> weights = {1, 2, 1};
    std::cout << "Avg: " << calculate_weighted_average(vals, weights) << std::endl;
    return 0;
}
EOF

    cat << 'EOF' > run_test.sh
#!/bin/bash
make clean && make
./monitor test_input.txt
if [ $? -eq 0 ]; then
    echo "Success"
    exit 0
else
    echo "Crash"
    exit 1
fi
EOF
    chmod +x run_test.sh

    git add Makefile main.cpp run_test.sh
    git commit -m "C0: Initial commit"
    GOOD_COMMIT=$(git rev-parse HEAD)

    # C1: Add file reading
    cat << 'EOF' > main.cpp
#include <iostream>
#include <vector>
#include <fstream>

double calculate_weighted_average(const std::vector<int>& values, const std::vector<int>& weights) {
    double sum = 0;
    double weight_sum = 0;
    for (size_t i = 0; i < values.size(); ++i) {
        sum += values[i] * weights[i];
        weight_sum += weights[i];
    }
    return sum / weight_sum;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    std::ifstream infile(argv[1]);
    int v, w;
    std::vector<int> vals, weights;
    while (infile >> v >> w) {
        vals.push_back(v);
        weights.push_back(w);
    }
    std::cout << "Avg: " << calculate_weighted_average(vals, weights) << std::endl;
    return 0;
}
EOF
    git add main.cpp
    git commit -m "C1: Read from file"

    # C2: Broken build
    cat << 'EOF' > main.cpp
#include <iostream>
#include <fstream>

double calculate_weighted_average(const std::vector<int>& values, const std::vector<int>& weights) {
    double sum = 0;
    double weight_sum = 0;
    for (size_t i = 0; i < values.size(); ++i) {
        sum += values[i] * weights[i];
        weight_sum += weights[i];
    }
    return sum / weight_sum;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    std::ifstream infile(argv[1]);
    int v, w;
    std::vector<int> vals, weights;
    while (infile >> v >> w) {
        vals.push_back(v);
        weights.push_back(w);
    }
    std::cout << "Avg: " << calculate_weighted_average(vals, weights) << std::endl;
    return 0;
}
EOF
    git add main.cpp
    git commit -m "C2: Refactor includes"

    # C3: Fix build
    sed -i '1i #include <vector>' main.cpp
    git add main.cpp
    git commit -m "C3: Fix build"

    # C4: Introduce the bug
    cat << 'EOF' > main.cpp
#include <vector>
#include <iostream>
#include <fstream>

double calculate_weighted_average(const std::vector<int>& values, const std::vector<int>& weights) {
    double sum = 0;
    double weight_sum = 0;
    for (size_t i = 0; i < values.size(); ++i) {
        // BUG: if weight is 0, this causes division by zero error in the loop!
        int normalized = values[i] / weights[i]; 
        sum += normalized * weights[i];
        weight_sum += weights[i];
    }
    return sum / weight_sum;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    std::ifstream infile(argv[1]);
    int v, w;
    std::vector<int> vals, weights;
    while (infile >> v >> w) {
        vals.push_back(v);
        weights.push_back(w);
    }
    std::cout << "Avg: " << calculate_weighted_average(vals, weights) << std::endl;
    return 0;
}
EOF
    git add main.cpp
    git commit -m "C4: Optimize weighted calc"
    BAD_COMMIT=$(git rev-parse HEAD)

    # C5: Add logging
    echo "// logging added" >> main.cpp
    git add main.cpp
    git commit -m "C5: Add logging"

    cat << 'EOF' > test_input.txt
100 1
200 2
150 0
300 1
EOF

    echo "Good commit: $GOOD_COMMIT" > /tmp/commits.txt
    echo "Bad commit: $BAD_COMMIT" >> /tmp/commits.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user