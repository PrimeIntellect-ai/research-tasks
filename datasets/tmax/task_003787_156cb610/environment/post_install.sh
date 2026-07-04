apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/audit_generator.cpp
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

uint16_t compute_hash(const std::string& data) {
    uint16_t sum = 0;
    for (char c : data) {
        sum = (sum + c) % 65535;
    }
    return sum;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <log_file>\n";
        return 1;
    }

    std::ifstream infile(argv[1]);
    if (!infile) {
        std::cerr << "Error opening file.\n";
        return 1;
    }

    std::stringstream buffer;
    buffer << infile.rdbuf();
    std::string log_content = buffer.str();

    if (compute_hash(log_content) != 25000) {
        std::cerr << "Invalid checksum\n";
        return 1;
    }

    std::ofstream outfile("audit_report.html");
    outfile << "<html><body><p>" << log_content << "</p></body></html>\n";
    outfile.close();

    std::cout << "Report generated.\n";
    return 0;
}
EOF

    chmod -R 777 /home/user