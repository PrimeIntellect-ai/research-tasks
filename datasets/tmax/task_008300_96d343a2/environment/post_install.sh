apt-get update && apt-get install -y python3 python3-pip g++ valgrind
    pip3 install pytest

    mkdir -p /home/user/sim_daemon

    cat << 'EOF' > /home/user/sim_daemon/sim_server.cpp
#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>

struct TrajectoryState {
    double time;
    double value;
    TrajectoryState(double t) : time(t), value(t * t) {}
};

void run_simulation(double target_time) {
    std::vector<TrajectoryState*> states;
    double time = 0.0;
    double dt = 0.1;

    // BUG: floating point equality check
    while (time != target_time) {
        states.push_back(new TrajectoryState(time));
        time += dt;

        // Safety break
        if (states.size() > 1000) {
            break;
        }
    }

    std::cout << "Simulation finished. Generated " << states.size() << " states." << std::endl;
    // BUG: memory leak, states are never deleted
}

int main(int argc, char* argv[]) {
    const char* env = std::getenv("SIM_ENV");
    if (!env || std::string(env) != "production") {
        std::cerr << "Error: SIM_ENV is not set to production." << std::endl;
        return 1;
    }

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl;
        return 1;
    }

    std::ifstream infile(argv[1]);
    double target;
    while (infile >> target) {
        run_simulation(target);
    }

    return 0;
}
EOF

    cat << 'EOF' > /home/user/sim_daemon/build.sh
#!/bin/bash
# SIM_ENV needs to be set and exported here!

g++ -O2 -g sim_server.cpp -o sim_server
EOF
    chmod +x /home/user/sim_daemon/build.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user