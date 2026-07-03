apt-get update && apt-get install -y python3 python3-pip git g++ gdb
    pip3 install pytest

    git config --global user.email "admin@example.com"
    git config --global user.name "Admin"

    mkdir -p /home/user/suspicious_daemon
    cd /home/user/suspicious_daemon
    git init

    cat << 'EOF' > service.cpp
#include <iostream>
#include <thread>
#include <vector>
#include <mutex>

std::vector<int> data_buffer;
std::mutex mtx;

void safe_process() {
    std::lock_guard<std::mutex> lock(mtx);
    data_buffer.push_back(1);
}

int main() {
    std::vector<std::thread> workers;
    for (int i=0; i<10; ++i) {
        workers.emplace_back([](){
            for(int j=0; j<100; ++j) {
                safe_process();
            }
        });
    }
    for (auto& w : workers) w.join();
    return 0;
}
EOF

    git add service.cpp
    git commit -m "Initial commit"

    # Create 15 dummy commits
    for i in {1..7}; do
        echo "// Dummy comment $i" >> service.cpp
        git commit -am "Dummy commit $i"
    done

    # Introduce the bug at commit 8
    cat << 'EOF' > service.cpp
#include <iostream>
#include <thread>
#include <vector>
#include <mutex>

std::vector<int> data_buffer;
std::mutex mtx;

void unsafe_cleanup() {
    // BUG: Missing lock, race condition on clear
    if (!data_buffer.empty()) {
        data_buffer.clear();
    }
}

void safe_process() {
    std::lock_guard<std::mutex> lock(mtx);
    data_buffer.push_back(1);
}

void trigger_payload() {
    unsafe_cleanup();
}

int main() {
    std::vector<std::thread> workers;
    for (int i=0; i<10; ++i) {
        workers.emplace_back([](){
            for(int j=0; j<1000; ++j) {
                safe_process();
                if (j % 100 == 0) trigger_payload();
            }
        });
    }
    for (auto& w : workers) w.join();
    return 0;
}
EOF
    git commit -am "Add cleanup routine"
    BAD_COMMIT=$(git rev-parse HEAD)
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    # Create remaining commits
    for i in {9..15}; do
        echo "// Dummy comment $i" >> service.cpp
        git commit -am "Dummy commit $i"
    done

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user