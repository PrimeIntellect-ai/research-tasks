apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        ffmpeg \
        g++ \
        e2fsprogs \
        e2tools \
        extundelete

    pip3 install pytest Pillow

    mkdir -p /app /opt /home/user

    # Generate video
    cat << 'EOF' > /tmp/gen_video.py
from PIL import Image
import os
os.makedirs('/tmp/frames', exist_ok=True)
for i in range(300):
    img = Image.new('RGB', (100, 100), color='black')
    if (50 <= i <= 60) or (120 <= i <= 130) or (200 <= i <= 219):
        for x in range(20):
            for y in range(20):
                img.putpixel((x,y), (255,0,0))
    img.save(f'/tmp/frames/frame_{i:03d}.png')
EOF
    python3 /tmp/gen_video.py
    ffmpeg -framerate 30 -i /tmp/frames/frame_%03d.png -c:v libx264 -pix_fmt yuv420p /app/flight_dashboard.mp4
    rm -rf /tmp/frames /tmp/gen_video.py

    # Generate drone_data.img
    dd if=/dev/zero of=/app/drone_data.img bs=1M count=10
    mkfs.ext4 -F /app/drone_data.img
    cat << 'EOF' > /tmp/telemetry_raw.log
SEQ:003 INFO Nav
SEQ:001 WARN Sensor
SEQ:002 ERROR Comms
EOF
    e2cp /tmp/telemetry_raw.log /app/drone_data.img:/
    e2rm /app/drone_data.img:/telemetry_raw.log
    rm /tmp/telemetry_raw.log

    # Generate legacy_decoder
    cat << 'EOF' > /tmp/legacy_decoder.cpp
#include <iostream>
#include <string>
#include <cstdint>
#include <cstring>

int main() {
    std::string input;
    while (std::cin >> input) {
        uint64_t val;
        if (sscanf(input.c_str(), "%lx", &val) == 1) {
            double d;
            std::memcpy(&d, &val, sizeof(d));
            float f = static_cast<float>(d);
            std::cout << f * 1.5 << "\n";
        }
    }
    return 0;
}
EOF
    g++ -O2 /tmp/legacy_decoder.cpp -o /app/legacy_decoder
    rm /tmp/legacy_decoder.cpp

    # Generate oracle_decoder
    cat << 'EOF' > /tmp/oracle_decoder.cpp
#include <iostream>
#include <string>
#include <cstdint>
#include <cstring>
#include <iomanip>

int main() {
    std::string input;
    while (std::cin >> input) {
        uint64_t val;
        if (sscanf(input.c_str(), "%lx", &val) == 1) {
            double d;
            std::memcpy(&d, &val, sizeof(d));
            std::cout << std::fixed << std::setprecision(6) << d * 1.5 << "\n";
        }
    }
    return 0;
}
EOF
    g++ -O2 /tmp/oracle_decoder.cpp -o /opt/oracle_decoder
    rm /tmp/oracle_decoder.cpp

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user