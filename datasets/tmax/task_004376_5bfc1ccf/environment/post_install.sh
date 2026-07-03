apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest Pillow

    apt-get install -y g++ tesseract-ocr

    mkdir -p /app

    cat << 'EOF' > /app/generate_image.py
from PIL import Image, ImageDraw
img = Image.new('RGB', (600, 100), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10, 40), "ROOT=0 TARGET=14 BAND_MIN=5 BAND_MAX=12", fill=(0, 0, 0))
img.save('/app/system_params.png')
EOF
    python3 /app/generate_image.py

    cat << 'EOF' > /app/sensor_graph.txt
15 16
0 1
1 2
2 3
3 4
4 14
0 5
5 6
6 7
7 14
0 8
8 9
9 10
10 11
11 12
12 13
13 14
EOF

    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

int main() {
    int N = 64;
    vector<double> y(N);
    double sum_x = 0, sum_y = 0, sum_xy = 0, sum_xx = 0;
    for (int i = 0; i < N; ++i) {
        if (!(cin >> y[i])) return 0;
        double x = i;
        sum_x += x;
        sum_y += y[i];
        sum_xy += x * y[i];
        sum_xx += x * x;
    }
    double m = (N * sum_xy - sum_x * sum_y) / (N * sum_xx - sum_x * sum_x);
    double c = (sum_y - m * sum_x) / N;

    int band_min = 5, band_max = 12;
    double max_mag = -1;
    int max_bin = -1;
    for (int k = band_min; k <= band_max; ++k) {
        double re = 0, im = 0;
        for (int n = 0; n < N; ++n) {
            double angle = -2.0 * M_PI * k * n / N;
            re += y[n] * cos(angle);
            im += y[n] * sin(angle);
        }
        double mag = sqrt(re * re + im * im);
        if (mag > max_mag) {
            max_mag = mag;
            max_bin = k;
        }
    }

    int shortest_path = 4;
    cout << fixed << setprecision(4) << m << " " << c << " " << max_bin << " " << shortest_path << endl;
    return 0;
}
EOF

    g++ -std=c++17 -O3 /app/oracle.cpp -o /app/oracle_feature_extractor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user