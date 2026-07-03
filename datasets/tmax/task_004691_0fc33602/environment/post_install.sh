apt-get update && apt-get install -y python3 python3-pip g++ gdb
    pip3 install pytest numpy scipy

    mkdir -p /app

    cat << 'EOF' > /app/processor.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <cstring>
#include <cstdint>
#include <cassert>

// Secret generated at runtime
char* session_id = nullptr;

struct WavHeader {
    char riff[4]; int32_t flength; char wave[4]; char fmt[4];
    int32_t chunk_size; int16_t format_tag; int16_t num_chans;
    int32_t srate; int32_t bytes_per_sec; int16_t bytes_per_samp;
    int16_t bits_per_samp; char data[4]; int32_t dlength;
};

std::vector<int16_t> read_wav(const char* path) {
    std::ifstream in(path, std::ios::binary);
    WavHeader h;
    in.read((char*)&h, sizeof(h));
    std::vector<int16_t> samples(h.dlength / 2);
    in.read((char*)samples.data(), h.dlength);
    return samples;
}

std::vector<double> compute_rolling_energy(const std::vector<int16_t>& samples, int window_size) {
    std::vector<double> energy(samples.size(), 0.0);
    // INTENTIONAL BOTTLENECK: O(N * W)
    for (size_t i = 0; i < samples.size(); ++i) {
        double sum_sq = 0;
        int count = 0;
        for (size_t j = 0; j < window_size && (i + j) < samples.size(); ++j) {
            sum_sq += static_cast<double>(samples[i + j]) * samples[i + j];
            count++;
        }
        energy[i] = std::sqrt(sum_sq / count);
    }
    return energy;
}

std::vector<int8_t> delta_encode(const std::vector<double>& energy) {
    std::vector<int8_t> encoded;
    encoded.reserve(energy.size());
    double prev = 0;
    for (size_t i = 0; i < energy.size(); ++i) {
        double diff = energy[i] - prev;
        // INTENTIONAL BUG: Sudden massive energy diff causes out-of-bounds or overflow logic
        // We simulate a segfault by indexing out of bounds if diff is extremely large
        int index = static_cast<int>(diff / 100.0);
        if (index > 50) {
            // Force crash
            int* bad_ptr = nullptr;
            *bad_ptr = 42; 
        }

        int8_t val = static_cast<int8_t>(std::max(-128.0, std::min(127.0, diff)));
        encoded.push_back(val);
        prev = energy[i];
    }
    return encoded;
}

int main(int argc, char** argv) {
    if (argc < 3) return 1;
    session_id = new char[17];
    std::strcpy(session_id, "SES-9928-PERF-01"); // Hidden session ID

    auto samples = read_wav(argv[1]);
    auto energy = compute_rolling_energy(samples, 1024);
    auto encoded = delta_encode(energy);

    std::ofstream out(argv[2], std::ios::binary);
    out.write((char*)encoded.data(), encoded.size());
    return 0;
}
EOF

    cat << 'EOF' > /tmp/generate_wav.py
import numpy as np
import scipy.io.wavfile as wavfile

sample_rate = 44100
duration = 30
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
samples = (np.sin(2 * np.pi * 440 * t) * 1000).astype(np.int16)
spike_start = int(15 * sample_rate)
spike_end = int(15.1 * sample_rate)
samples[spike_start:spike_end] = 32767

wavfile.write('/app/transmission.wav', sample_rate, samples)
EOF

    python3 /tmp/generate_wav.py
    rm /tmp/generate_wav.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user