apt-get update && apt-get install -y python3 python3-pip g++ ffmpeg
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user

    # Create oracle source code
    cat << 'EOF' > /app/oracle_filter.cpp
#include <iostream>
#include <vector>
#include <iomanip>

int main() {
    std::vector<double> window;
    double val;
    while (std::cin >> val) {
        window.push_back(val);
        if (window.size() > 10) {
            window.erase(window.begin());
        }
        double sum = 0;
        for (double v : window) sum += v;
        double mean = sum / window.size();
        double var = 0;
        for (double v : window) var += (v - mean) * (v - mean);
        var /= window.size();
        std::cout << std::fixed << std::setprecision(6) << var << "\n";
    }
    return 0;
}
EOF

    # Compile oracle
    g++ -O3 /app/oracle_filter.cpp -o /app/oracle_filter
    rm /app/oracle_filter.cpp

    # Create buggy source code
    cat << 'EOF' > /home/user/anomaly_filter.cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<float> window;
    float val;
    while (std::cin >> val) {
        std::vector<float>* leak = new std::vector<float>(1000); // memory leak
        window.push_back(val);
        if (window.size() > 11) { // off by one error
            window.erase(window.begin());
        }
        float sum = 0;
        float sum_sq = 0;
        for (float v : window) {
            sum += v;
            sum_sq += v * v;
        }
        float mean = sum / window.size();
        float var = (sum_sq / window.size()) - (mean * mean); // precision loss
        std::cout << var << "\n";
    }
    return 0;
}
EOF

    # Create test video
    ffmpeg -f lavfi -i testsrc=duration=5:size=320x240:rate=10 -c:v libx264 /app/camera_feed.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user