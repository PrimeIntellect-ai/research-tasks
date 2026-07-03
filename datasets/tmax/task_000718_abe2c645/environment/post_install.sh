apt-get update && apt-get install -y python3 python3-pip g++ gdb
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/src

    cat << 'EOF' > /home/user/src/sim_engine.cpp
#include <iostream>
#include <cstring>

struct SessionData {
    char session_id[32];
    double delta;
    double distance;
};

// VULNERABILITY: delta is passed as float, causing precision loss for very small doubles
double calculate_speed(double distance, float delta) {
    // 1e-40 cast to float becomes 0.0f, triggering a divide by zero
    return distance / delta;
}

int main() {
    SessionData s;
    std::strcpy(s.session_id, "TXN-8842-OMEGA-PROTOCOL");
    s.delta = 1e-40; 
    s.distance = 500.0;

    double speed = calculate_speed(s.distance, s.delta);
    std::cout << "Speed: " << speed << std::endl;
    return 0;
}
EOF

    cd /home/user
    g++ -g -O0 /home/user/src/sim_engine.cpp -o /home/user/sim_engine

    # Generate core dump using gdb to bypass container ulimit/sysctl restrictions
    gdb -batch -ex "break calculate_speed" -ex "run" -ex "next" -ex "generate-core-file /home/user/core" -ex "kill" /home/user/sim_engine || true

    chmod -R 777 /home/user