apt-get update && apt-get install -y python3 python3-pip cargo g++
    pip3 install pytest

    # Create log_pipeline project
    mkdir -p /home/user/log_pipeline/src

    cat << 'EOF' > /home/user/log_pipeline/Cargo.toml
[package]
name = "log_pipeline"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    touch /home/user/log_pipeline/src/query.rs
    touch /home/user/log_pipeline/src/parser.rs
    touch /home/user/log_pipeline/src/analytics.rs
    touch /home/user/log_pipeline/src/worker.rs

    # Create analytics_oracle
    mkdir -p /app
    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
int main() {
    double count = 0, mean = 0, M2 = 0, newValue;
    while (std::cin >> newValue) {
        count += 1;
        double delta = newValue - mean;
        mean += delta / count;
        double delta2 = newValue - mean;
        M2 += delta * delta2;
    }
    if (count < 2) std::cout << 0 << std::endl;
    else std::cout << M2 / (count - 1) << std::endl;
    return 0;
}
EOF
    g++ -O3 -s /app/oracle.cpp -o /app/analytics_oracle
    rm /app/oracle.cpp

    # Create corpora
    mkdir -p /app/corpora/evil
    mkdir -p /app/corpora/clean

    echo '{"a":{"b":{"c":{"d":{"e":"bomb"}}}}}' > /app/corpora/evil/bomb1.log
    echo '{"very_long_key_that_exceeds_sixty_four_characters_in_length_1234567890":"value"}' > /app/corpora/evil/bomb2.log

    echo '{"a":{"b":"normal"}}' > /app/corpora/clean/normal1.log
    echo '{"short_key":"value"}' > /app/corpora/clean/normal2.log

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app