apt-get update && apt-get install -y python3 python3-pip ffmpeg g++
    pip3 install pytest

    # Setup oracle and fixture
    mkdir -p /app /opt/oracle

    # Generate dummy calibration.mp4 using ffmpeg (100 frames, 10x10 resolution to make math easy)
    ffmpeg -y -f lavfi -i testsrc=size=10x10:rate=10 -vframes 100 /app/calibration.mp4 >/dev/null 2>&1

    # Write oracle C++ code
    cat << 'EOF' > /opt/oracle/main.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include <iomanip>

using namespace std;

// Hardcoded weights for the generated video (in a real scenario, this would be computed)
// For simplicity in this truth setup, we dynamically extract them to a header or read them.
// Wait, the oracle must extract them too. We will use a script to generate weights.
EOF

    # Pre-calculate weights from the generated video for the oracle
    ffmpeg -i /app/calibration.mp4 -pix_fmt gray -f image2pipe -vcodec rawvideo - > /tmp/raw_video.bin 2>/dev/null

    cat << 'EOF' > /opt/oracle/gen_weights.py
import sys
with open('/tmp/raw_video.bin', 'rb') as f:
    data = f.read()
frames = 100
pixels = 100 # 10x10
weights = []
for i in range(frames):
    frame_data = data[i*pixels:(i+1)*pixels]
    w = sum(frame_data) % 256
    weights.append(w)
print(weights)
with open('/opt/oracle/weights.h', 'w') as f:
    f.write("int W[100] = {")
    f.write(",".join(map(str, weights)))
    f.write("};\n")
EOF
    python3 /opt/oracle/gen_weights.py

    # Complete oracle code
    cat << 'EOF' >> /opt/oracle/main.cpp
#include "weights.h"

struct Row {
    int frame_index;
    string node_id;
    double value;
};

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    ifstream file(argv[1]);
    string line;
    map<string, vector<Row>> data;

    while (getline(file, line)) {
        if(line.empty()) continue;
        stringstream ss(line);
        string f_idx_str, node, val_str;
        getline(ss, f_idx_str, ',');
        getline(ss, node, ',');
        getline(ss, val_str, ',');

        Row r;
        r.frame_index = stoi(f_idx_str);
        r.node_id = node;
        r.value = stod(val_str);
        data[node].push_back(r);
    }

    for (auto& pair : data) {
        auto& rows = pair.second;
        sort(rows.begin(), rows.end(), [](const Row& a, const Row& b) {
            return a.frame_index < b.frame_index;
        });

        for (size_t i = 0; i < rows.size(); ++i) {
            double sum = 0;
            int count = 0;
            for (int j = i; j >= 0 && count < 3; --j, ++count) {
                sum += rows[j].value * W[rows[j].frame_index];
            }
            cout << rows[i].frame_index << "," << rows[i].node_id << "," 
                 << fixed << setprecision(2) << sum << "\n";
        }
    }
    return 0;
}
EOF
    g++ -O3 /opt/oracle/main.cpp -o /opt/oracle/analyzer_oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user