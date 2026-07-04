apt-get update && apt-get install -y python3 python3-pip espeak ffmpeg build-essential

pip3 install pytest
pip3 install torch --index-url https://download.pytorch.org/whl/cpu
pip3 install openai-whisper

mkdir -p /app
espeak -w /app/model_parameters.wav "The sequence scoring parameters are as follows: alpha is two point five, beta is zero point five, and the window size is four."

cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <string>
#include <vector>
#include <cmath>

int main() {
    std::string seq;
    if (!(std::cin >> seq)) return 0;

    double alpha = 2.5;
    double beta = 0.5;
    int window_size = 4;

    std::vector<double> signal;
    for (char c : seq) {
        int val = 0;
        if (c == 'A') val = 1;
        else if (c == 'C') val = 2;
        else if (c == 'G') val = 3;
        else if (c == 'T') val = 4;

        signal.push_back(val * alpha + beta);
    }

    for (size_t i = 0; i < signal.size(); ++i) {
        double sum = 0;
        int count = 0;
        for (size_t j = (i >= window_size - 1 ? i - window_size + 1 : 0); j <= i; ++j) {
            sum += signal[j];
            count++;
        }
        std::cout << (int)(sum / count) << (i == signal.size() - 1 ? "" : " ");
    }
    std::cout << std::endl;
    return 0;
}
EOF

g++ -O3 /app/oracle.cpp -o /app/oracle_seq_score

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app