apt-get update && apt-get install -y python3 python3-pip g++ imagemagick tesseract-ocr
    pip3 install pytest

    # Create /app directory and generate the image
    mkdir -p /app
    convert -size 600x100 xc:white -font DejaVu-Sans -pointsize 24 -fill black -draw "text 10,50 'SCHEMA_VERSION=v4.2 TOLERANCE=0.05'" /app/experiment_schema.png

    # Create /opt/oracle directory and the oracle binary
    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/pipeline_ref.cpp
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

int main() {
    string line;
    double sum_metrics = 0.0;
    int count = 0;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        cout << "SCHEMA_VERSION=v4.2 TOLERANCE=0.05" << endl;
        cout << "Record: " << line << endl;
    }
    return 0;
}
EOF
    g++ -O3 /opt/oracle/pipeline_ref.cpp -o /opt/oracle/pipeline_ref
    rm /opt/oracle/pipeline_ref.cpp
    chmod +x /opt/oracle/pipeline_ref

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user