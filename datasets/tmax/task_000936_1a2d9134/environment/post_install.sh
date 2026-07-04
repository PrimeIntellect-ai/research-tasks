apt-get update && apt-get install -y python3 python3-pip g++ zlib1g-dev tesseract-ocr imagemagick
    pip3 install pytest

    mkdir -p /app

    # Generate schema.png
    convert -size 800x200 xc:white -font DejaVu-Sans -pointsize 24 -fill black -gravity center -draw "text 0,0 'WAL MAGIC SEQUENCE: 0x41 0x52 0x54 0x49'" /app/schema.png

    # Write oracle source
    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <map>
#include <zlib.h>
#include <cstdint>
#include <string>

using namespace std;

int main() {
    gzFile f = gzdopen(fileno(stdin), "rb");
    if (!f) return 1;

    char magic[4];
    if (gzread(f, magic, 4) != 4 || string(magic, 4) != "ARTI") {
        cout << "INVALID_MAGIC\n";
        gzclose(f);
        return 1;
    }

    map<uint16_t, uint32_t> state;
    uint8_t op;
    while (gzread(f, &op, 1) == 1) {
        if (op == 0x0A) {
            uint16_t id;
            uint32_t size;
            if (gzread(f, &id, 2) != 2) break;
            if (gzread(f, &size, 4) != 4) break;
            if (state.find(id) == state.end()) state[id] = size;
        } else if (op == 0x0B) {
            uint16_t id;
            if (gzread(f, &id, 2) != 2) break;
            state.erase(id);
        } else if (op == 0x0C) {
            uint16_t id;
            uint32_t size;
            if (gzread(f, &id, 2) != 2) break;
            if (gzread(f, &size, 4) != 4) break;
            if (state.find(id) != state.end()) state[id] = size;
        } else {
            break;
        }
    }
    gzclose(f);

    for (auto const& [id, size] : state) {
        printf("%u -> %u bytes\n", id, size);
    }
    return 0;
}
EOF

    # Compile oracle
    g++ -O3 /app/oracle.cpp -lz -o /app/oracle_parser
    chmod +x /app/oracle_parser
    rm /app/oracle.cpp

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user