apt-get update && apt-get install -y python3 python3-pip git g++ valgrind tcpdump
pip3 install pytest scapy

useradd -m -s /bin/bash user || true

# 1. Setup Environment Misconfiguration
mkdir -p /home/user/service_repo/src
echo '{"mode": "production"}' > /home/user/service_repo/actual_config.json

# 2. Setup Git Repository and C++ Code
cd /home/user/service_repo
git init
git config user.email "dev@example.com"
git config user.name "Dev"

cat << 'EOF' > src/server.cpp
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>

void process_payload(const std::string& payload) {
    if (payload.find("NORMAL") != std::string::npos) {
        // Normal processing
        return;
    }
}

int main(int argc, char** argv) {
    const char* env = std::getenv("CONFIG_ENV");
    if (!env || std::string(env) != "production") {
        std::cerr << "Error: CONFIG_ENV not set to production" << std::endl;
        return 1;
    }
    // Simulate reading from network
    if (argc > 1) {
        process_payload(argv[1]);
    }
    return 0;
}
EOF

git add .
git commit -m "Initial commit: basic server"

# Commit 2 (The Buggy Commit)
cat << 'EOF' > src/server.cpp
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>

void process_payload(const std::string& payload) {
    if (payload.find("NORMAL") != std::string::npos) {
        return;
    }

    if (payload.find("MALFORMED_X99_ABORT") != std::string::npos) {
        char* buffer = new char[1024 * 1024]; // 1MB allocation
        std::strcpy(buffer, payload.c_str());
        // BUG: Forgot to delete[] buffer;
        return;
    }
}

int main(int argc, char** argv) {
    const char* env = std::getenv("CONFIG_ENV");
    if (!env || std::string(env) != "production") {
        std::cerr << "Error: CONFIG_ENV not set to production" << std::endl;
        return 1;
    }
    if (argc > 1) {
        process_payload(argv[1]);
    }
    return 0;
}
EOF

git add .
git commit -m "Add handling for malformed packets"
BUGGY_COMMIT=$(git rev-parse HEAD)

# Commit 3 (Unrelated change)
echo "// Added comment for logging" >> src/server.cpp
git add .
git commit -m "Add logging comment"

# Save the buggy commit to a hidden file for verification script if needed
echo $BUGGY_COMMIT > /tmp/.buggy_commit

# 3. Create the PCAP file
cat << 'EOF' > /tmp/gen_pcap.py
from scapy.all import *

packets = []
# Normal packet
packets.append(IP(dst="127.0.0.1")/TCP(dport=8888)/Raw(load="NORMAL_REQUEST_1"))
# Normal packet
packets.append(IP(dst="127.0.0.1")/TCP(dport=8888)/Raw(load="NORMAL_REQUEST_2"))
# The Trigger packet
packets.append(IP(dst="127.0.0.1")/TCP(dport=8888)/Raw(load="MALFORMED_X99_ABORT"))
# Normal packet
packets.append(IP(dst="127.0.0.1")/TCP(dport=8888)/Raw(load="NORMAL_REQUEST_3"))

wrpcap('/home/user/capture.pcap', packets)
EOF

python3 /tmp/gen_pcap.py
rm /tmp/gen_pcap.py

chmod -R 777 /home/user