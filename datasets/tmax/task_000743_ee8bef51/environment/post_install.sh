apt-get update && apt-get install -y python3 python3-pip curl gcc make ffmpeg
    pip3 install pytest

    # Install Node.js
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs

    mkdir -p /app
    mkdir -p /home/user/api
    mkdir -p /home/user/analyzer

    # Create package.json with conflicting dependencies
    cat << 'EOF' > /home/user/api/package.json
{
  "name": "api",
  "version": "1.0.0",
  "dependencies": {
    "express": "4.18.2",
    "apollo-server-express": "3.13.0",
    "graphql": "16.8.1"
  }
}
EOF

    # Generate synthetic video with red screen at frame 42
    # 150 frames at 25fps = 6 seconds
    ffmpeg -f lavfi -i "color=c=black:s=320x240:d=6" -vf "drawbox=x=0:y=0:w=320:h=240:color=red@1:t=fill:enable='eq(n\,42)'" -vcodec libx264 -pix_fmt yuv420p -r 25 -y /app/terminal_e2e.mp4

    # Create oracle analyzer
    cat << 'EOF' > /app/oracle_analyzer.c
#include <stdio.h>
#include <stdint.h>

int main() {
    uint64_t total_score = 0;
    uint8_t rgb[3];
    while (fread(rgb, 1, 3, stdin) == 3) {
        if (rgb[0] > (rgb[1] + rgb[2])) {
            total_score += (rgb[0] - rgb[1] - rgb[2]);
        }
    }
    printf("%llu\n", (unsigned long long)(total_score % 1000003));
    return 0;
}
EOF
    gcc -O3 /app/oracle_analyzer.c -o /app/oracle_analyzer
    strip /app/oracle_analyzer

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user