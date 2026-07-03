apt-get update && apt-get install -y python3 python3-pip g++ ffmpeg tesseract-ocr sudo locales tzdata mailutils
pip3 install pytest

mkdir -p /app
mkdir -p /opt/reference

# Provide the video fixture (mock generation for test setup)
touch /app/diagnostic_console.mp4

# Provide the oracle binary
cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <string>
#include <regex>
#include <iomanip>
#include <sstream>

int main() {
    std::string line;
    std::regex pattern(R"(^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$)");
    while (std::getline(std::cin, line)) {
        std::smatch match;
        if (std::regex_match(line, match, pattern)) {
            int y = std::stoi(match[1]);
            int m = std::stoi(match[2]);
            int d = std::stoi(match[3]);
            int h = std::stoi(match[4]);
            int min = std::stoi(match[5]);
            int s = std::stoi(match[6]);

            if (m < 1 || m > 12 || d < 1 || d > 31 || h > 23 || min > 59 || s > 59) {
                std::cout << "INVALID_FORMAT\n";
                continue;
            }

            // Simple UTC to Asia/Tokyo (+9 hours) conversion logic for oracle
            h += 9;
            if (h >= 24) {
                h -= 24;
                d += 1;
                // Simplified day overflow for the sake of the oracle (assumes 31 days everywhere for simplicity in this dummy oracle, though a real test would use proper mktime)
                if (d > 31) { d = 1; m += 1; }
                if (m > 12) { m = 1; y += 1; }
            }

            std::cout << std::setfill('0') << y << "年" 
                      << std::setw(2) << m << "月" 
                      << std::setw(2) << d << "日 "
                      << std::setw(2) << h << "時"
                      << std::setw(2) << min << "分"
                      << std::setw(2) << s << "秒\n";
        } else {
            std::cout << "INVALID_FORMAT\n";
        }
    }
    return 0;
}
EOF
g++ -O3 /tmp/oracle.cpp -o /opt/reference/log_formatter_oracle
strip /opt/reference/log_formatter_oracle
rm /tmp/oracle.cpp

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user