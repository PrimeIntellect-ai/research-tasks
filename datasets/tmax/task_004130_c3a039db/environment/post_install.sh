apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        g++ \
        imagemagick \
        fonts-dejavu-core \
        tesseract-ocr \
        libtesseract-dev

    pip3 install pytest

    mkdir -p /app
    useradd -m -s /bin/bash user || true

    # Create oracle source code
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <iomanip>

struct LogEntry {
    std::string service;
    long long timestamp;
    std::string message;
};

bool compareLogs(const LogEntry& a, const LogEntry& b) {
    return a.timestamp < b.timestamp;
}

int main() {
    std::vector<LogEntry> logs;
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        std::stringstream ss(line);
        std::string service, ts_str, message;
        if (std::getline(ss, service, '|') &&
            std::getline(ss, ts_str, '|') &&
            std::getline(ss, message)) {
            logs.push_back({service, std::stoll(ts_str), message});
        }
    }

    std::sort(logs.begin(), logs.end(), compareLogs);

    for (const auto& log : logs) {
        time_t ts = log.timestamp;
        struct tm *tm_info = gmtime(&ts);
        char buffer[26];
        strftime(buffer, 26, "%Y-%m-%d %H:%M:%S", tm_info);
        std::cout << "[" << buffer << "] <" << log.service << "> - " << log.message << "\n";
    }
    return 0;
}
EOF

    # Compile oracle and strip it
    g++ -O3 -o /app/oracle_bin /tmp/oracle.cpp
    strip /app/oracle_bin
    rm /tmp/oracle.cpp

    # Create buggy source code
    cat << 'EOF' > /home/user/buggy_aggregator.cpp
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <thread>
#include <mutex>
#include <algorithm>

struct LogEntry {
    std::string service;
    long long timestamp;
    std::string message;
};

std::vector<LogEntry> logs;
std::mutex mtx1;
std::mutex mtx2;

void process_logs(const std::vector<std::string>& lines) {
    for (const auto& line : lines) {
        std::stringstream ss(line);
        std::string service, ts_str, message;
        if (std::getline(ss, service, '|') &&
            std::getline(ss, ts_str, '|') &&
            std::getline(ss, message)) {

            std::lock_guard<std::mutex> lock1(mtx1);
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            std::lock_guard<std::mutex> lock2(mtx2);

            logs.push_back({service, std::stoll(ts_str), message});
        }
    }
}

void process_logs_reverse(const std::vector<std::string>& lines) {
    for (const auto& line : lines) {
        std::stringstream ss(line);
        std::string service, ts_str, message;
        if (std::getline(ss, service, '|') &&
            std::getline(ss, ts_str, '|') &&
            std::getline(ss, message)) {

            std::lock_guard<std::mutex> lock2(mtx2);
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            std::lock_guard<std::mutex> lock1(mtx1);

            logs.push_back({service, std::stoll(ts_str), message});
        }
    }
}

int main() {
    std::vector<std::string> all_lines;
    std::string line;
    while (std::getline(std::cin, line)) {
        if (!line.empty()) all_lines.push_back(line);
    }

    size_t half = all_lines.size() / 2;
    std::vector<std::string> part1(all_lines.begin(), all_lines.begin() + half);
    std::vector<std::string> part2(all_lines.begin() + half, all_lines.end());

    std::thread t1(process_logs, part1);
    std::thread t2(process_logs_reverse, part2);

    t1.join();
    t2.join();

    std::sort(logs.begin(), logs.end(), [](const LogEntry& a, const LogEntry& b) {
        return a.timestamp < b.timestamp;
    });

    for (const auto& log : logs) {
        std::cout << log.service << ": " << log.message << " at " << log.timestamp << "\n";
    }
    return 0;
}
EOF

    # Generate ticket screenshot
    convert -size 900x200 xc:white -font DejaVu-Sans -pointsize 20 -fill black \
        -draw "text 10,50 'MIGRATION NOTE: The new log format must strictly follow this template:'" \
        -draw "text 10,100 '[YYYY-MM-DD HH:MM:SS] <SERVICE> - MSG'" \
        /app/ticket_screenshot.png

    chmod -R 777 /home/user
    chmod -R 777 /app