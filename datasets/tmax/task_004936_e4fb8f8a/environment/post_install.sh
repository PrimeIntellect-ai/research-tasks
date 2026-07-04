apt-get update && apt-get install -y python3 python3-pip g++ coreutils
    pip3 install pytest

    mkdir -p /home/user/project/libmath
    cd /home/user/project

    # Create the shared library source
    cat << 'EOF' > /home/user/project/libmath/custom_math.cpp
#include <string>
void process_math(const std::string& input) {
    if (input.find("CRASH_TRIGGER") != std::string::npos) {
        int* ptr = nullptr;
        *ptr = 42; // Segmentation fault
    }
}
EOF

    # Compile the shared library
    g++ -shared -fPIC -o /home/user/project/libmath/libcustom_math.so /home/user/project/libmath/custom_math.cpp

    # Create the generator source
    cat << 'EOF' > /home/user/project/generator.cpp
#include <iostream>
#include <string>

extern void process_math(const std::string&);

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        process_math(line);
    }
    return 0;
}
EOF

    # Create the flawed build script
    cat << 'EOF' > /home/user/project/build.sh
#!/bin/bash

# Compiles successfully
g++ -o generator generator.cpp -L./libmath -lcustom_math

# Fails here because LD_LIBRARY_PATH is not set, meaning libcustom_math.so cannot be found.
# Once LD_LIBRARY_PATH=./libmath is added, it will fail on line 734 due to the crash.
while read -r p; do
   echo "$p" | base64 -d | ./generator
done < fuzz_corpus.txt
EOF
    chmod +x /home/user/project/build.sh

    # Generate the fuzzed corpus with the hidden crash trigger
    for i in $(seq 1 1000); do
        if [ $i -eq 734 ]; then
            printf "MATH_EXPR:CRASH_TRIGGER:59" | base64 >> /home/user/project/fuzz_corpus.txt
        else
            printf "MATH_EXPR:VALID_DATA:%d" "$i" | base64 >> /home/user/project/fuzz_corpus.txt
        fi
    done

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user