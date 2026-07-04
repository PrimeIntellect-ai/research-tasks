apt-get update && apt-get install -y python3 python3-pip g++ ffmpeg imagemagick fonts-dejavu-core wget
    pip3 install pytest

    # Create directories
    mkdir -p /home/user/api_processor/build
    mkdir -p /home/user/api_processor/src
    mkdir -p /home/user/api_processor/include
    mkdir -p /app
    mkdir -p /opt

    # Download JSON library
    wget -q https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp -O /home/user/api_processor/include/json.hpp

    # Create build.sh with syntax error
    cat << 'EOF' > /home/user/api_processor/build.sh
#!/bin/bash
mkdir -p build
g++ -o build/processor src/main.cpp src/migration.cpp -I include --std=c++14
EOF
    chmod +x /home/user/api_processor/build.sh

    # Create main.cpp
    cat << 'EOF' > /home/user/api_processor/src/main.cpp
#include <iostream>
#include <string>
#include "json.hpp"

extern std::string migrate(const std::string& input);

int main() {
    std::string line;
    if (std::getline(std::cin, line)) {
        std::cout << migrate(line) << std::endl;
    }
    return 0;
}
EOF

    # Create migration.cpp
    cat << 'EOF' > /home/user/api_processor/src/migration.cpp
#include <string>
#include "json.hpp"

using json = nlohmann::json;

std::string migrate(const std::string& input) {
    // TODO: implement migration logic
    return "{}";
}
EOF

    # Create video frames and video
    mkdir -p /tmp/frames
    # Fix Imagemagick policy to allow text/draw
    sed -i 's/rights="none" pattern="PATTERN"/rights="read|write" pattern="PATTERN"/' /etc/ImageMagick-6/policy.xml || true

    convert -size 640x480 xc:black -fill white -pointsize 20 -gravity center -draw "text 0,0 'user_ident (int) -> uid (string, converted)'" /tmp/frames/001.png
    convert -size 640x480 xc:black -fill white -pointsize 20 -gravity center -draw "text 0,0 'registration_timestamp (string) -> created_at (string, exact copy)'" /tmp/frames/002.png
    convert -size 640x480 xc:black -fill white -pointsize 20 -gravity center -draw "text 0,0 'payload_data (string) -> data.raw (nested object)'" /tmp/frames/003.png
    convert -size 640x480 xc:black -fill white -pointsize 20 -gravity center -draw "text 0,0 'status_code (int) -> isActive (bool, true if > 0 else false)'" /tmp/frames/004.png
    convert -size 640x480 xc:black -fill white -pointsize 20 -gravity center -draw "text 0,0 'DROP all other fields'" /tmp/frames/005.png

    ffmpeg -framerate 1 -i /tmp/frames/%03d.png -c:v libx264 -r 1 -pix_fmt yuv420p /app/migration_rules.mp4
    rm -rf /tmp/frames

    # Create oracle processor
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <string>
#include "json.hpp"

using json = nlohmann::json;

int main() {
    std::string line;
    if (std::getline(std::cin, line)) {
        try {
            json in = json::parse(line);
            json out = json::object();
            if (in.contains("user_ident") && in["user_ident"].is_number_integer()) {
                out["uid"] = std::to_string(in["user_ident"].get<int>());
            }
            if (in.contains("registration_timestamp") && in["registration_timestamp"].is_string()) {
                out["created_at"] = in["registration_timestamp"];
            }
            if (in.contains("payload_data") && in["payload_data"].is_string()) {
                out["data"] = json::object();
                out["data"]["raw"] = in["payload_data"];
            }
            if (in.contains("status_code") && in["status_code"].is_number_integer()) {
                out["isActive"] = in["status_code"].get<int>() > 0;
            }
            std::cout << out.dump() << std::endl;
        } catch (...) {
            std::cout << "{}" << std::endl;
        }
    }
    return 0;
}
EOF
    g++ -o /opt/oracle_processor /tmp/oracle.cpp -I /home/user/api_processor/include --std=c++17
    strip /opt/oracle_processor
    rm /tmp/oracle.cpp

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user