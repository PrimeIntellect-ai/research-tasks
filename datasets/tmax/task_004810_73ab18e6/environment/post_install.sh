apt-get update && apt-get install -y python3 python3-pip build-essential gdb
    pip3 install pytest

    mkdir -p /home/user/sim

    cat << 'EOF' > /home/user/sim/main.cpp
#include <iostream>
#include <iomanip>
#include "simulation.h"

int main() {
    double init_val = 3.141592653589793;
    double res = run_simulation(init_val);
    std::cout << std::setprecision(16) << res << std::endl;
    return 0;
}
EOF

    cat << 'EOF' > /home/user/sim/simulation.h
#ifndef SIMULATION_H
#define SIMULATION_H

double run_simulation(double val);

#endif
EOF

    cat << 'EOF' > /home/user/sim/simulation.cpp
#include "simulation.h"

double step1(double val) {
    return val * 2.0;
}

double step2(double val) {
    float temp = val; // Precision loss here
    return temp / 2.0;
}

double step3(double val) {
    return val + 0.0;
}

double run_simulation(double val) {
    val = step1(val);
    val = step2(val);
    val = step3(val);
    return val;
}
EOF

    cat << 'EOF' > /home/user/sim/Makefile
CXX = g++
CXXFLAGS = -g -Wall -O0

all: sim_run

sim_run: main.o simulation.o
	$(CXX) $(CXXFLAGS) -o sim_run main.o simulation.o

main.o: main.cpp simulation.h
	$(CXX) $(CXXFLAGS) -c main.cpp

simulation.o: simulation.cpp simulation.h
	$(CXX) $(CXXFLAGS) -c simulation.cpp

clean:
	rm -f *.o sim_run
EOF

    cd /home/user/sim && make

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user