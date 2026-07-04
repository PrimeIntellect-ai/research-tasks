apt-get update && apt-get install -y python3 python3-pip git g++ make
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/math_calc/src
    cd /home/user/math_calc

    cat << 'EOF' > Makefile
all: calc

calc: src/calc.cpp
	g++ -O2 src/calc.cpp -o calc

clean:
	rm -f calc
EOF

    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    # Initial correct state
    cat << 'EOF' > src/calc.cpp
#include <iostream>
#include <cstdlib>

long long compute(int n) {
    long long res = 0;
    for (int i = 0; i < n; i++) {
        res += (long long)i * i;
    }
    return res;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    int n = std::atoi(argv[1]);
    std::cout << compute(n) << std::endl;
    return 0;
}
EOF

    git add Makefile src/calc.cpp
    git commit -m "Initial commit"

    # Create dummy commits
    for i in $(seq 1 70); do
        echo "// Dummy comment $i" >> src/calc.cpp
        git commit -am "Dummy commit $i"
    done

    # Secret injection
    echo "API_KEY=X89B-SECR-9921" > secret_config.env
    git add secret_config.env
    git commit -m "Add config"

    # Remove secret
    git rm secret_config.env
    git commit -m "Remove config"

    # More dummy commits
    for i in $(seq 71 100); do
        echo "// Dummy comment $i" >> src/calc.cpp
        git commit -am "Dummy commit $i"
    done

    # Introduce build failure
    cat << 'EOF' > src/calc.cpp
// Missing iostream
#include <cstdlib>

long long compute(int n) {
    long long res = 0;
    for (int i = 0; i < n; i++) {
        res += (long long)i * i;
    }
    return res;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    int n = std::atoi(argv[1]);
    std::cout << compute(n) << "\n";
    return 0;
}
EOF
    git commit -am "Refactor imports"

    for i in $(seq 101 105); do
        echo "// Dummy comment $i" >> src/calc.cpp
        git commit -am "Dummy commit $i"
    done

    # Fix build but introduce math bug
    cat << 'EOF' > src/calc.cpp
#include <iostream>
#include <cstdlib>

long long compute(int n) {
    long long res = 0;
    for (int i = 0; i < n; i++) {
        res += i * i; // BUG: integer overflow
    }
    return res;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    int n = std::atoi(argv[1]);
    std::cout << compute(n) << std::endl;
    return 0;
}
EOF
    git commit -am "Fix build and optimize loop"

    BAD_COMMIT=$(git rev-parse HEAD)
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    # More dummy commits
    for i in $(seq 106 160); do
        echo "// Dummy comment $i" >> src/calc.cpp
        git commit -am "Dummy commit $i"
    done

    chown -R user:user /home/user/math_calc
    chmod -R 777 /home/user