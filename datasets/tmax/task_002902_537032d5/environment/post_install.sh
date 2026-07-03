apt-get update && apt-get install -y python3 python3-pip imagemagick ffmpeg g++
    pip3 install pytest

    mkdir -p /app

    # Generate video
    mkdir -p /tmp/frames
    for i in {0..299}; do
        if [ "$i" -eq 142 ]; then
            convert -size 64x64 canvas:red /tmp/frames/frame_$(printf "%03d" $i).png
        else
            convert -size 64x64 canvas:black /tmp/frames/frame_$(printf "%03d" $i).png
        fi
    done
    ffmpeg -y -framerate 30 -i /tmp/frames/frame_%03d.png -c:v libx264 -pix_fmt yuv420p /app/curation_log.mp4
    rm -rf /tmp/frames

    # Generate oracle
    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>
#include <cstring>

using namespace std;

#pragma pack(push, 1)
struct Header {
    char magic[4];
    uint32_t size;
    uint16_t flags;
    char name[16];
};
#pragma pack(pop)

int main() {
    uint16_t F = 142;
    while (true) {
        Header h;
        if (!cin.read(reinterpret_cast<char*>(&h), sizeof(h))) {
            if (cin.eof() && cin.gcount() == 0) return 0;
            cout << "[ERROR] Incomplete record\n";
            return 1;
        }
        if (strncmp(h.magic, "ARTF", 4) != 0) {
            cout << "[ERROR] Invalid magic\n";
            return 1;
        }
        if (h.size > 1024) {
            cout << "[ERROR] Size too large\n";
            return 1;
        }
        vector<char> data(h.size);
        if (h.size > 0) {
            if (!cin.read(data.data(), h.size)) {
                cout << "[ERROR] Incomplete record\n";
                return 1;
            }
        }

        if (h.flags == F) continue;

        string nameStr(h.name, 16);
        size_t nullPos = nameStr.find('\0');
        if (nullPos != string::npos) nameStr = nameStr.substr(0, nullPos);

        if (h.flags & 0x01) {
            cout << "[VALID] " << nameStr << " - " << h.size << " bytes\n";
        } else {
            cout << "[IGNORED] " << nameStr << "\n";
        }
    }
    return 0;
}
EOF
    g++ -O3 /app/oracle.cpp -o /app/oracle_curator

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user