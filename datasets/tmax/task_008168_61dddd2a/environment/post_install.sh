apt-get update && apt-get install -y python3 python3-pip git clang make
pip3 install pytest

git config --global user.email "test@example.com"
git config --global user.name "Test User"

mkdir -p /home/user/kvstore
cd /home/user/kvstore
git init

cat << 'EOF' > Makefile
CXX = clang++
CXXFLAGS = -O1 -g -fsanitize=fuzzer,address
TARGET = fuzz_kvstore

all: $(TARGET)

$(TARGET): kvstore.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -f $(TARGET)
EOF

cat << 'EOF' > kvstore.cpp
#include <string>
#include <map>
#include <iostream>
#include <vector>

std::map<std::string, std::string> store;

void process_request(const std::string& input) {
    if (input.empty()) return;

    // Simple mock processing
    if (input[0] == 'S' && input.size() > 4) {
        store["key"] = input.substr(1);
    } else if (input[0] == 'G') {
        std::string val = store["key"];
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    std::string input(reinterpret_cast<const char*>(Data), Size);
    process_request(input);
    return 0;
}
EOF

git add Makefile kvstore.cpp
git commit -m "Initial commit: basic KV store setup"
GOOD_COMMIT=$(git rev-parse HEAD)

# Commit 2 (Safe feature)
cat << 'EOF' > kvstore.cpp
#include <string>
#include <map>
#include <iostream>
#include <vector>

std::map<std::string, std::string> store;

void process_request(const std::string& input) {
    if (input.empty()) return;

    if (input[0] == 'S' && input.size() > 4) {
        store["key"] = input.substr(1);
    } else if (input[0] == 'G') {
        std::string val = store["key"];
    } else if (input[0] == 'D') {
        store.clear();
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    std::string input(reinterpret_cast<const char*>(Data), Size);
    process_request(input);
    return 0;
}
EOF
git add kvstore.cpp
git commit -m "Add delete operation"

# Commit 3 (The bad commit - Memory Leak)
cat << 'EOF' > kvstore.cpp
#include <string>
#include <map>
#include <iostream>
#include <vector>

std::map<std::string, std::string> store;

void process_request(const std::string& input) {
    if (input.empty()) return;

    if (input[0] == 'S' && input.size() > 4) {
        store["key"] = input.substr(1);
    } else if (input[0] == 'G') {
        std::string val = store["key"];
    } else if (input[0] == 'D') {
        store.clear();
    } else if (input.find("LEAK") != std::string::npos) {
        // Intentional memory leak introduced here
        char* buffer = new char[1024];
        buffer[0] = 'X';
        // Missing delete[] buffer;
    }
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    std::string input(reinterpret_cast<const char*>(Data), Size);
    process_request(input);
    return 0;
}
EOF
git add kvstore.cpp
git commit -m "Add advanced string parsing for diagnostics"
BAD_COMMIT=$(git rev-parse HEAD)

# Commit 4 (Unrelated change)
cat << 'EOF' > Makefile
CXX = clang++
CXXFLAGS = -O1 -g -fsanitize=fuzzer,address -Wall
TARGET = fuzz_kvstore

all: $(TARGET)

$(TARGET): kvstore.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -f $(TARGET)
EOF
git add Makefile
git commit -m "Update Makefile to include Wall"

echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user