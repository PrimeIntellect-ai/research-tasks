apt-get update && apt-get install -y python3 python3-pip g++ tesseract-ocr imagemagick fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Create the specification image
    # We use ImageMagick to render the text into an image
    # Note: Policy.xml in imagemagick might restrict PDF/etc, but usually PNG creation from text is fine.
    convert -size 1800x400 xc:white -font DejaVu-Sans -pointsize 24 -fill black -annotate +20+40 "DATA PROCESSING SPECIFICATION
Input format: CSV from stdin with 3 columns: ID (integer), Category (single uppercase character A-Z), Value (float).
Step 1. Structured Filter: Ignore any row where ID is negative.
Step 2. Stratified Sampling: Group the stream by Category. For each Category, only keep every 2nd valid row (i.e., keep the 2nd, 4th, 6th... occurrence of that Category).
Step 3. Windowed Aggregation: For the sampled rows within each Category, calculate the moving sum of the last 3 sampled Values for that Category (including the current one).
Step 4. Output format: Print \"Category,SampledValue,MovingSum\" to stdout." /app/spec.png

    # Create oracle source code
    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <string>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <deque>

using namespace std;

struct CategoryState {
    int count = 0;
    deque<float> window;
};

int main() {
    string line;
    unordered_map<char, CategoryState> states;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        string id_str, cat_str, val_str;
        if (!getline(ss, id_str, ',')) continue;
        if (!getline(ss, cat_str, ',')) continue;
        if (!getline(ss, val_str, ',')) continue;

        int id;
        try { id = stoi(id_str); } catch(...) { continue; }
        if (id < 0) continue;

        char cat = cat_str[0];
        float val;
        try { val = stof(val_str); } catch(...) { continue; }

        auto& state = states[cat];
        state.count++;
        if (state.count % 2 == 0) {
            state.window.push_back(val);
            if (state.window.size() > 3) {
                state.window.pop_front();
            }
            float sum = 0;
            for (float v : state.window) sum += v;
            cout << cat << "," << val << "," << sum << "\n";
        }
    }
    return 0;
}
EOF

    # Compile the oracle binary
    g++ -O3 -std=c++17 /app/oracle.cpp -o /app/oracle_bin
    rm /app/oracle.cpp

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user