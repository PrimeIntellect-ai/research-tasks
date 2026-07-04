apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <cstring>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 3) return 1;
    ifstream in(argv[1], ios::binary);
    ofstream out(argv[2]);
    if (!in) return 1;

    char magic[4];
    if (!in.read(magic, 4) || memcmp(magic, "DAT\0", 4) != 0) return 0;

    while (true) {
        streampos start_pos = in.tellg();
        uint8_t type;
        if (!in.read((char*)&type, 1)) break;

        if (type == 0x10 || type == 0x11 || type == 0x30) {
            uint64_t ts;
            uint16_t len;
            if (!in.read((char*)&ts, 8) || !in.read((char*)&len, 2)) {
                in.clear();
                in.seekg(start_pos + streamoff(1));
                continue;
            }

            if (type == 0x10 && len != 4) {
                in.clear();
                in.seekg(start_pos + streamoff(1));
                continue;
            }
            if (type == 0x11 && len != 8) {
                in.clear();
                in.seekg(start_pos + streamoff(1));
                continue;
            }

            vector<uint8_t> payload(len);
            if (len > 0) {
                if (!in.read((char*)payload.data(), len)) {
                    in.clear();
                    in.seekg(start_pos + streamoff(1));
                    continue;
                }
            }

            uint8_t checksum;
            if (!in.read((char*)&checksum, 1)) {
                in.clear();
                in.seekg(start_pos + streamoff(1));
                continue;
            }

            uint8_t calc_csum = type;
            for (int i=0; i<8; ++i) calc_csum ^= ((uint8_t*)&ts)[i];
            for (int i=0; i<2; ++i) calc_csum ^= ((uint8_t*)&len)[i];
            for (int i=0; i<len; ++i) calc_csum ^= payload[i];

            if (calc_csum == checksum) {
                if (type == 0x10) {
                    int32_t val;
                    memcpy(&val, payload.data(), 4);
                    out << ts << "|INT32|" << val << "\n";
                } else if (type == 0x11) {
                    int64_t val;
                    memcpy(&val, payload.data(), 8);
                    out << ts << "|INT64|" << val << "\n";
                } else if (type == 0x30) {
                    out << ts << "|TEXT|";
                    for (int i=0; i<len; ++i) {
                        if (payload[i] == '\\') out << "\\\\";
                        else if (payload[i] == '\n') out << "\\n";
                        else out << (char)payload[i];
                    }
                    out << "\n";
                }
            } else {
                in.clear();
                in.seekg(start_pos + streamoff(1));
            }
        } else {
            in.clear();
            in.seekg(start_pos + streamoff(1));
        }
    }
    return 0;
}
EOF

    g++ -O2 /app/oracle.cpp -o /app/log_parser_oracle
    strip /app/log_parser_oracle
    rm /app/oracle.cpp

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user