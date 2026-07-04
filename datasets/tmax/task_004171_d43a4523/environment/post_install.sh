apt-get update && apt-get install -y python3 python3-pip g++ make
    pip3 install pytest

    mkdir -p /app/fastcsv-1.0

    cat << 'EOF' > /app/fastcsv-1.0/fastcsv.h
#ifndef FASTCSV_H
#define FASTCSV_H
#include <string>
#include <vector>
#include <istream>

namespace fastcsv {
    class Parser {
    public:
        static std::vector<std::vector<std::string>> parse(std::istream& in);
    };
}
#endif
EOF

    cat << 'EOF' > /app/fastcsv-1.0/fastcsv.cpp
#include "fastcsv.h"
#include <sstream>

namespace fastcsv {
    std::vector<std::vector<std::string>> Parser::parse(std::istream& in) {
        std::vector<std::vector<std::string>> result;
        std::string line;
        while (std::getline(in, line)) {
            std::vector<std::string> row;
            std::stringstream ss(line);
            std::string cell;
            while (std::getline(ss, cell, ',')) {
                row.push_back(cell);
            }
            if (!row.empty()) result.push_back(row);
        }
        return result;
    }
}
EOF

    cat << 'EOF' > /app/fastcsv-1.0/Makefile
CXX = gcc
CXXFLAGS = -O2

all: libfastcsv.a

libfastcsv.a: fastcsv.o
	ar rcs libfastcsv.a fastcsv.o

fastcsv.o: fastcsv.cpp fastcsv.h
	$(CXX) $(CXXFLAGS) -c fastcsv.cpp -o fastcsv.o

clean:
	rm -f *.o *.a
EOF

    cat << 'EOF' > /app/oracle_process.cpp
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <iomanip>

int main() {
    std::string line;
    std::getline(std::cin, line); // skip header
    std::map<std::string, std::pair<double, int>> aggregates;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string id, group, fx_str, fy_str;
        std::getline(ss, id, ',');
        std::getline(ss, group, ',');
        std::getline(ss, fx_str, ',');
        std::getline(ss, fy_str, ',');

        double fx = std::stod(fx_str);
        double fy = std::stod(fy_str);
        double z = 0.8 * fx + 0.2 * fy;

        aggregates[group].first += z;
        aggregates[group].second += 1;
    }

    std::cout << "group,mean_z\n";
    for (const auto& kv : aggregates) {
        double mean = kv.second.first / kv.second.second;
        std::cout << kv.first << "," << std::fixed << std::setprecision(3) << mean << "\n";
    }
    return 0;
}
EOF

    g++ -O2 -std=c++11 /app/oracle_process.cpp -o /app/oracle_process

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user