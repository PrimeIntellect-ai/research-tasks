apt-get update && apt-get install -y python3 python3-pip ffmpeg g++ build-essential
    pip3 install pytest

    mkdir -p /app

    # Create oracle C++ source
    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <sstream>
#include <iomanip>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string line;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        long long timestamp;
        string pattern;
        int n;
        if (!(ss >> timestamp >> pattern >> n)) continue;
        regex re(pattern);
        for (int i = 0; i < n; ++i) {
            double val;
            if (!(ss >> val)) break;
            stringstream val_ss;
            val_ss << fixed << setprecision(3) << val;
            string val_str = val_ss.str();
            if (regex_match(val_str, re)) {
                cout << timestamp << "," << i << "," << val_str << "\n";
            }
        }
    }
    return 0;
}
EOF

    # Compile the oracle
    g++ -O3 /app/oracle.cpp -o /app/oracle_processor
    chmod +x /app/oracle_processor

    # Create subtitle file
    cat << 'EOF' > /app/sub.srt
1
00:00:00,000 --> 00:00:01,000
1700000000 ^100\.[0-9]{3}$ 5 100.123 99.999 100.000 10.000 100.999

2
00:00:01,000 --> 00:00:02,000
1700000001 ^-?[0-9]+\.500$ 4 12.500 -5.500 12.501 0.500
EOF

    # Create dummy video with subtitle stream
    ffmpeg -f lavfi -i color=c=black:s=16x16:d=2 -i /app/sub.srt -c:v libx264 -c:s mov_text /app/server_monitor.mp4

    # Clean up intermediate files
    rm /app/oracle.cpp /app/sub.srt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user