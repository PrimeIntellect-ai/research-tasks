apt-get update && apt-get install -y python3 python3-pip g++ gdb
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/suspicious.cpp
#include <iostream>
#include <vector>
#include <fstream>

int main() {
    long long A = 17;
    long long B = 29;
    long long M = 999983;
    std::ofstream log("/home/user/app.log");

    for (int n = 1; n <= 500000; ++n) {
        long long next_A = (13 * A + 19 * B) % M;
        long long next_B = (23 * A + 31 * B) % M;
        A = next_A;
        B = next_B;

        if (n <= 50) {
            log << "n=" << n << " A=" << A << " B=" << B << "\n";
        }

        // Suspicious trigger that causes a crash
        long long trigger = (A * B) % 200000;
        if (trigger > 180000) {
            int* p = nullptr;
            *p = 42; // Deliberate segfault
        }
    }
    return 0;
}
EOF

    chmod -R 777 /home/user