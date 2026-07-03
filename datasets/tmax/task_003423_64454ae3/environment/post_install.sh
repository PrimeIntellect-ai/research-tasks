apt-get update && apt-get install -y python3 python3-pip protobuf-compiler libprotobuf-dev g++ imagemagick fonts-liberation tesseract-ocr
    pip3 install pytest protobuf Pillow

    mkdir -p /app

    # Generate the legacy_schema.png
    # Temporarily remove ImageMagick security policy that blocks label/text creation if it exists
    rm -f /etc/ImageMagick-6/policy.xml
    convert -background white -fill black -font Liberation-Mono -pointsize 24 label:'syntax = "proto2";\n\nmessage LegacyLog {\n  required int32 id = 1;\n  required bytes py2_message = 2;\n}' /app/legacy_schema.png

    # Create the oracle migrator
    cat << 'EOF' > /app/legacy.proto
syntax = "proto2";

message LegacyLog {
  required int32 id = 1;
  required bytes py2_message = 2;
}
EOF

    cat << 'EOF' > /app/modern.proto
syntax = "proto3";

message ModernLog {
  int32 log_id = 1;
  string utf8_message = 2;
}
EOF

    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <string>
#include "legacy.pb.h"
#include "modern.pb.h"

int main() {
    LegacyLog legacy;
    if (!legacy.ParseFromIstream(&std::cin)) {
        return 1;
    }

    ModernLog modern;
    modern.set_log_id(legacy.id());

    std::string utf8_str;
    for (unsigned char c : legacy.py2_message()) {
        if (c < 0x80) {
            utf8_str.push_back(c);
        } else {
            utf8_str.push_back(0xC0 | (c >> 6));
            utf8_str.push_back(0x80 | (c & 0x3F));
        }
    }
    modern.set_utf8_message(utf8_str);

    if (!modern.SerializeToOstream(&std::cout)) {
        return 1;
    }
    return 0;
}
EOF

    cd /app
    protoc --cpp_out=. legacy.proto modern.proto
    g++ -O3 oracle.cpp legacy.pb.cc modern.pb.cc -o /app/oracle_migrator -lprotobuf
    chmod +x /app/oracle_migrator

    # Cleanup temporary source files
    rm /app/legacy.proto /app/modern.proto /app/oracle.cpp /app/legacy.pb.* /app/modern.pb.*

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user