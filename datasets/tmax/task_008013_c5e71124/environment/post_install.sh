apt-get update && apt-get install -y python3 python3-pip git g++ coreutils
    pip3 install pytest

    mkdir -p /home/user
    cd /home/user

    # Create the base64 test input
    echo -n "1.123456789 #2.123456789 3.123456789" | base64 > /home/user/test_input.b64

    # Initialize repository
    mkdir -p /home/user/data_processor
    cd /home/user/data_processor
    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    # Good C++ code
    cat << 'EOF' > process_sensor_data.cpp
#include <iostream>
#include <string>
#include <cmath>

double parse_val(const std::string& s) {
    std::string clean = "";
    for (char c : s) {
        if (isdigit(c) || c == '.' || c == '-') clean += c;
    }
    if (clean.empty()) return 0.0;
    return std::stod(clean);
}

int main() {
    std::string line;
    double sum = 0.0;
    while (std::cin >> line) {
        sum += parse_val(line);
    }
    std::cout.precision(10);
    std::cout << sum << std::endl;
    return 0;
}
EOF

    git add process_sensor_data.cpp
    git commit -m "Initial commit: robust parsing"
    git tag v1.0

    # Generate commits 1 to 136
    for i in $(seq 1 136); do
        echo "Update $i" > dummy.txt
        git add dummy.txt
        git commit -m "Dummy commit $i"
    done

    # Introduce the bad commit at 137
    cat << 'EOF' > process_sensor_data.cpp
#include <iostream>
#include <string>
#include <cmath>

double parse_val(const std::string& s) {
    try {
        return (double)std::stof(s);
    } catch (...) {
        return 0.0;
    }
}

int main() {
    std::string line;
    double sum = 0.0;
    while (std::cin >> line) {
        sum += parse_val(line);
    }
    std::cout.precision(10);
    std::cout << sum << std::endl;
    return 0;
}
EOF

    git add process_sensor_data.cpp
    git commit -m "Optimize parsing logic"
    BAD_COMMIT=$(git rev-parse HEAD)
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    # Generate commits 138 to 200
    for i in $(seq 138 200); do
        echo "Update $i" > dummy.txt
        git add dummy.txt
        git commit -m "Dummy commit $i"
    done

    git tag v2.0

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user