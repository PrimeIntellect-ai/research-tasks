apt-get update && apt-get install -y python3 python3-pip g++ imagemagick fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Generate the parameter image
    convert -size 400x100 xc:white -font DejaVu-Sans -pointsize 24 -fill black -annotate +20+50 'PARAMETER: 7.42' /app/parameter.png

    # Create and compile the oracle
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

int main() {
    std::string line;
    double sum = 0.0;
    double c = 0.0;
    double multiplier = 7.42;

    while (std::getline(std::cin, line)) {
        if (line.size() >= 38 && line.substr(0, 6) == "ATOM  ") {
            std::string x_str = line.substr(30, 8);
            double x = 0.0;
            try {
                x = std::stod(x_str);
            } catch (...) {
                x = 0.0;
            }
            double val = x * multiplier;
            double y = val - c;
            double t = sum + y;
            c = (t - sum) - y;
            sum = t;
        }
    }
    std::cout << std::fixed << std::setprecision(8) << sum << std::endl;
    return 0;
}
EOF

    g++ -O3 /tmp/oracle.cpp -o /app/oracle
    rm /tmp/oracle.cpp

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app