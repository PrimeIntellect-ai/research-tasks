apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user/tests

    # Create the buggy C++ source code
    cat << 'EOF' > /app/log_analyzer.cpp
#include <iostream>
#include <string>
#include <cmath>
#include <map>

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        size_t n = line.length();
        size_t i = 0;

        // Buggy loop simulating O(N^3) convergence failure
        while (i < n) {
            if ((unsigned char)line[i] > 127 && i + 4 < n && line.substr(i+1, 4) == "____") {
                // Artificial delay to simulate the hang (> 1 second)
                for(volatile int j = 0; j < 300000000; ++j) {}
                i += 5;
            } else {
                i++;
            }
        }

        std::map<char, int> counts;
        for (char c : line) counts[c]++;
        double entropy = 0.0;
        for (auto const& pair : counts) {
            double p = (double)pair.second / n;
            entropy -= p * std::log2(p);
        }
        std::cout << entropy << "\n";
    }
    return 0;
}
EOF

    # Compile and strip the binary
    g++ -O2 /app/log_analyzer.cpp -o /app/log_analyzer
    strip /app/log_analyzer
    rm /app/log_analyzer.cpp

    # Create sample logs
    cat << 'EOF' > /home/user/sample_logs.txt
127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
192.168.1.1 - - [11/Oct/2000:14:56:32 -0700] "GET /index.html HTTP/1.1" 200 1024
10.0.0.5 - admin [12/Oct/2000:15:57:33 -0700] "POST /login HTTP/1.1" 401 512
172.16.0.2 - - [13/Oct/2000:16:58:34 -0700] "GET /images/logo.png HTTP/1.1" 200 4096
192.168.2.10 - user [14/Oct/2000:17:59:35 -0700] "GET /api/data HTTP/1.1" 500 128
EOF

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user