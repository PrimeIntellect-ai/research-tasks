apt-get update && apt-get install -y python3 python3-pip build-essential cmake libeigen3-dev
    pip3 install pytest

    mkdir -p /app/fast_odesolver-1.2.0/src

    cat << 'EOF' > /app/fast_odesolver-1.2.0/CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(fast_odesolver)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(fast_odesolver src/solver.cpp)
target_include_directories(fast_odesolver PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
add_compile_options(-fPIC -Werror=return-type -DBROKEN_FLAG=1)
EOF

    cat << 'EOF' > /app/fast_odesolver-1.2.0/src/solver.cpp
#ifdef BROKEN_FLAG
#error "Platform not supported"
#endif

#include <vector>

void solve_ode() {
    // Dummy implementation
}
EOF

    mkdir -p /app/fast_odesolver-1.2.0/include
    cat << 'EOF' > /app/fast_odesolver-1.2.0/include/solver.h
#pragma once
void solve_ode();
EOF

    # Create dummy oracle
    cat << 'EOF' > /app/oracle_fit_source.cpp
#include <iostream>
int main() {
    return 0;
}
EOF
    g++ -o /app/oracle_fit /app/oracle_fit_source.cpp
    chmod +x /app/oracle_fit

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user