apt-get update && apt-get install -y python3 python3-pip g++ espeak curl
    pip3 install pytest

    mkdir -p /app

    # Generate speech.wav
    espeak -w /app/speech.wav "scientific computing with rust."

    # Generate projection matrix
    python3 -c "
import random
with open('/app/projection_matrix.txt', 'w') as f:
    for i in range(5):
        row = [f'{random.uniform(-1, 1):.4f}' for _ in range(16)]
        f.write(','.join(row) + '\n')
"

    # Create oracle in C++
    cat << 'EOF' > /app/oracle_extractor.cpp
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <algorithm>

using namespace std;

int main() {
    vector<float> input;
    float val;
    while (cin >> val) {
        input.push_back(val);
    }
    int N = input.size();
    if (N == 0) return 0;

    // 1. DFT for first 16 bins
    vector<float> mags(16, 0.0f);
    for (int k = 0; k < 16; ++k) {
        double re = 0, im = 0;
        for (int n = 0; n < N; ++n) {
            double angle = -2.0 * M_PI * k * n / N;
            re += input[n] * cos(angle);
            im += input[n] * sin(angle);
        }
        mags[k] = sqrt(re * re + im * im);
    }

    // 2. Matrix projection
    vector<vector<float>> proj(5, vector<float>(16, 0.0f));
    ifstream mfile("/app/projection_matrix.txt");
    string line;
    for (int i = 0; i < 5; ++i) {
        if (!getline(mfile, line)) break;
        stringstream ss(line);
        string cell;
        for (int j = 0; j < 16; ++j) {
            getline(ss, cell, ',');
            proj[i][j] = stof(cell);
        }
    }

    vector<float> features(5, 0.0f);
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 16; ++j) {
            features[i] += proj[i][j] * mags[j];
        }
    }

    // 3. Bootstrap
    int F = N / 128;
    vector<float> frame_energies(F, 0.0f);
    for (int f = 0; f < F; ++f) {
        for (int i = 0; i < 128; ++i) {
            float s = input[f * 128 + i];
            frame_energies[f] += s * s;
        }
    }

    unsigned long long X = 42;
    vector<float> means(1000, 0.0f);
    for (int b = 0; b < 1000; ++b) {
        float sum = 0;
        for (int i = 0; i < F; ++i) {
            X = (X * 1103515245ULL + 12345ULL) % 2147483648ULL;
            int idx = X % F;
            sum += frame_energies[idx];
        }
        means[b] = sum / F;
    }
    sort(means.begin(), means.end());
    float lower = means[25];
    float upper = means[975];

    cout << fixed << setprecision(4);
    for (int i = 0; i < 5; ++i) {
        cout << features[i] << (i == 4 ? "" : ",");
    }
    cout << "\n" << lower << "," << upper << "\n";

    return 0;
}
EOF

    g++ -O3 /app/oracle_extractor.cpp -o /app/oracle_extractor
    chmod +x /app/oracle_extractor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user