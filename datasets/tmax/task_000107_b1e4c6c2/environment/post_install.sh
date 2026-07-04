apt-get update && apt-get install -y python3 python3-pip g++ ffmpeg
    pip3 install pytest numpy opencv-python-headless

    mkdir -p /app

    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    std::ifstream file(argv[1], std::ios::binary);
    if (!file) return 1;

    std::vector<float> W(256, 0.1f);
    std::vector<float> X(256);

    while (file.read(reinterpret_cast<char*>(X.data()), 256 * sizeof(float))) {
        float y = 0.0f;
        for (int j = 0; j < 256; ++j) {
            y += X[j] * W[j];
        }
        float error = y - 1.0f;
        for (int j = 0; j < 256; ++j) {
            W[j] = W[j] - (0.001f * error * X[j]);
        }
    }

    for (int j = 0; j < 256; ++j) {
        printf("%.6f ", W[j]);
    }
    printf("\n");
    return 0;
}
EOF
    g++ -O3 /tmp/oracle.cpp -o /app/oracle_model
    chmod +x /app/oracle_model

    ffmpeg -f lavfi -i testsrc=duration=10:size=320x240:rate=30 -pix_fmt yuv420p /app/experiment.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user