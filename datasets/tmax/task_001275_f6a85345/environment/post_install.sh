apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        build-essential \
        zlib1g-dev \
        tesseract-ocr \
        imagemagick \
        fonts-dejavu-core

    pip3 install pytest

    mkdir -p /app/incoming/dir1 /app/incoming/dir2

    # Create the specification image
    cat << 'EOF' > /tmp/spec.txt
ARTIFACT STREAM SPECIFICATION
-----------------------------
The stream consists of packed metadata blocks.
To find a block, scan byte-by-byte for the Magic Sequence: 0x41 0x52 ('AR').
Once found:
1. Read the next 4 bytes as a 32-bit unsigned integer (Little Endian) representing the Compressed Length (N).
2. Read the next N bytes as a zlib-deflated (compressed) payload.
3. Attempt to decompress the payload.
   - If decompression succeeds, print the uncompressed string exactly as-is, followed by a newline ('\n').
   - If decompression fails, or if EOF is reached prematurely, discard the block, advance exactly 1 byte past the original 'A' (0x41) magic byte, and resume scanning.
EOF
    # Allow imagemagick to read the text file and write the image
    sed -i 's/rights="none" pattern="@\*"/rights="read" pattern="@\*"/' /etc/ImageMagick-6/policy.xml || true
    convert -size 800x400 xc:white -font DejaVu-Sans -pointsize 14 -fill black -annotate +10+20 "@/tmp/spec.txt" /app/magic_spec.png

    # Create the oracle extractor
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <zlib.h>

int main() {
    std::vector<uint8_t> buffer;
    uint8_t byte;
    while (std::cin.read(reinterpret_cast<char*>(&byte), 1)) {
        buffer.push_back(byte);
    }

    size_t i = 0;
    while (i + 5 < buffer.size()) {
        if (buffer[i] == 0x41 && buffer[i+1] == 0x52) {
            uint32_t len = buffer[i+2] | (buffer[i+3] << 8) | (buffer[i+4] << 16) | (buffer[i+5] << 24);
            if (i + 6 + len <= buffer.size()) {
                std::vector<uint8_t> uncompressed(len * 10 + 4096);
                uLongf destLen = uncompressed.size();
                int res = uncompress(uncompressed.data(), &destLen, buffer.data() + i + 6, len);
                if (res == Z_OK) {
                    std::cout.write(reinterpret_cast<char*>(uncompressed.data()), destLen);
                    std::cout << "\n";
                    i += 6 + len;
                    continue;
                }
            }
        }
        i++;
    }
    return 0;
}
EOF
    g++ -O3 /tmp/oracle.cpp -o /app/oracle_extractor -lz
    chmod +x /app/oracle_extractor

    # Create incoming files
    cat << 'EOF' > /tmp/make_files.py
import os
import zlib
import struct

def make_file(path, size, setuid, valid_paths):
    with open(path, 'wb') as f:
        f.write(os.urandom(500))
        for p in valid_paths:
            f.write(b'\x41\x52')
            comp = zlib.compress(p.encode())
            f.write(struct.pack('<I', len(comp)))
            f.write(comp)
            f.write(os.urandom(100))
        while f.tell() < size:
            f.write(os.urandom(100))
    if setuid:
        os.chmod(path, 0o4755)
    else:
        os.chmod(path, 0o0755)

make_file('/app/incoming/dir1/file1.bin', 2000, True, ['/tmp/path1', '/tmp/path2'])
make_file('/app/incoming/dir2/file2.bin', 500, True, ['/tmp/path3'])
make_file('/app/incoming/dir2/file3.bin', 1500, False, ['/tmp/path4'])
make_file('/app/incoming/dir1/file4.bin', 3000, True, ['/tmp/path5'])

for p in ['/tmp/path1', '/tmp/path2', '/tmp/path3', '/tmp/path4', '/tmp/path5']:
    with open(p, 'w') as f:
        f.write('dummy')
EOF
    python3 /tmp/make_files.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user