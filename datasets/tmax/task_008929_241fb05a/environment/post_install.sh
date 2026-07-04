apt-get update && apt-get install -y python3 python3-pip git cmake make g++ strace
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/math_sim/src
    cd /home/user/math_sim
    git init
    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    cat << 'EOF' > CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MathSim)
set(CMAKE_CXX_STANDARD 17)
find_package(Threads REQUIRED)
add_executable(math_sim src/main.cpp)
target_link_libraries(math_sim Threads::Threads)
EOF

    cat << 'EOF' > src/main.cpp
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <fstream>
#include <string>

std::atomic<uint64_t> global_sum{0};

void worker(uint64_t start, uint64_t end) {
    for (uint64_t i = start; i <= end; ++i) {
        global_sum += (i * i);
    }
}

int main() {
    std::ifstream config("/tmp/math_config.json");
    if (!config.is_open()) {
        std::cerr << "Error: config file missing!" << std::endl;
        return 1;
    }

    uint64_t N = 10000000;
    int num_threads = 4;
    std::vector<std::thread> threads;
    uint64_t chunk = N / num_threads;

    for (int i = 0; i < num_threads; ++i) {
        uint64_t start = i * chunk + 1;
        uint64_t end = (i == num_threads - 1) ? N : (i + 1) * chunk;
        threads.emplace_back(worker, start, end);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << global_sum.load() << std::endl;
    return 0;
}
EOF

    git add .
    git commit -m "Initial commit with correct atomic sum"

    for i in $(seq 1 130); do
        echo "// Dummy comment $i" >> src/main.cpp
        git commit -am "Dummy commit $i"
    done

    cat << 'EOF' > src/main.cpp
#include <iostream>
#include <vector>
#include <thread>
#include <fstream>
#include <string>

uint64_t global_sum = 0;

void worker(uint64_t start, uint64_t end) {
    for (uint64_t i = start; i <= end; ++i) {
        global_sum += (i * i);
    }
}

int main() {
    std::ifstream config("/tmp/math_config.json");
    if (!config.is_open()) {
        std::cerr << "Error: config file missing!" << std::endl;
        return 1;
    }

    uint64_t N = 10000000;
    int num_threads = 4;
    std::vector<std::thread> threads;
    uint64_t chunk = N / num_threads;

    for (int i = 0; i < num_threads; ++i) {
        uint64_t start = i * chunk + 1;
        uint64_t end = (i == num_threads - 1) ? N : (i + 1) * chunk;
        threads.emplace_back(worker, start, end);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << global_sum << std::endl;
    return 0;
}
EOF

    git commit -am "Optimize: remove atomic overhead"
    git rev-parse HEAD > /tmp/expected_bad_commit.txt

    for i in $(seq 133 199); do
        echo "// Another dummy comment $i" >> src/main.cpp
        git commit -am "Dummy commit $i"
    done

    cat << 'EOF' > CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MathSim)
set(CMAKE_CXX_STANDARD 17)
# Fictional dependency version conflict
find_package(Boost 1.99.0 REQUIRED)
find_package(Threads REQUIRED)
add_executable(math_sim src/main.cpp)
target_link_libraries(math_sim Threads::Threads)
EOF

    git commit -am "Update CMake to require Boost 1.99.0"

    chown -R user:user /home/user/math_sim
    chmod -R 777 /home/user