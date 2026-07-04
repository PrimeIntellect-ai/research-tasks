apt-get update && apt-get install -y python3 python3-pip gcc ffmpeg
pip3 install pytest

mkdir -p /home/user/sec_lib /home/user/go_legacy
cat << 'EOF' > /home/user/sec_lib/scanner.h
#ifndef SCANNER_H
#define SCANNER_H
#include <stdint.h>
struct frame_data {
    int32_t id;
    uint8_t hash[32];
};
float calculate_threat(struct frame_data *data);
#endif
EOF

cat << 'EOF' > /home/user/sec_lib/scanner.c
#include "scanner.h"
float calculate_threat(struct frame_data *data) {
    float score = (float)data->id * 0.001f;
    for(int i=0; i<32; i++) {
        score += (float)data->hash[i] / 255.0f;
    }
    while(score > 1.0f) score -= 1.0f;
    return score;
}
EOF

mkdir -p /app
gcc -shared -o /app/libsecscan.so -fPIC /home/user/sec_lib/scanner.c

cat << 'EOF' > /app/oracle_scanner.c
#include <stdio.h>
#include <stdlib.h>
#include "scanner.h"
int main() {
    struct frame_data fd;
    while(fread(&fd.id, 4, 1, stdin) == 1) {
        if(fread(fd.hash, 1, 32, stdin) != 32) break;
        float threat = calculate_threat(&fd);
        printf("Threat: %.4f\n", threat);
    }
    return 0;
}
EOF
gcc -o /app/oracle_scanner /app/oracle_scanner.c -L/app -lsecscan -Wl,-rpath=/app -I/home/user/sec_lib

ffmpeg -f lavfi -i testsrc=duration=10:size=640x480:rate=30 -c:v libx264 /app/surveillance.mp4 -y

cat << 'EOF' > /home/user/go_legacy/main.go
package main
import (
    "fmt"
    "go_legacy/processor" // Circular import!
)
func main() {
    fmt.Println("Starting...")
    processor.ProcessFrames()
}
EOF

cat << 'EOF' > /home/user/go_legacy/processor.go
package processor
import "go_legacy/main" // Circular import!
func ProcessFrames() {
    // Uses goroutines to pass structs
}
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app