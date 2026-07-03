apt-get update && apt-get install -y python3 python3-pip g++ tesseract-ocr imagemagick fonts-dejavu
    pip3 install pytest

    mkdir -p /app

    # Generate the formula image
    convert -size 600x100 xc:white -font DejaVu-Sans -pointsize 24 -fill black -draw "text 20,50 'result = (a * c + b * b) % 4096'" /app/formula.png

    # Create and compile the oracle
    cat << 'EOF' > /app/oracle_transform.cpp
#include <iostream>

int main() {
    long long a, b, c;
    while (std::cin >> a >> b >> c) {
        long long result = (a * c + b * b) % 4096;
        std::cout << result << std::endl;
    }
    return 0;
}
EOF
    g++ -O3 /app/oracle_transform.cpp -o /app/oracle_transform

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user