apt-get update && apt-get install -y python3 python3-pip gcc ffmpeg
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /app/oracle_analyzer.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    unsigned char buf[12288];
    size_t n = fread(buf, 1, 12288, f);
    fclose(f);
    if (n != 12288) {
        printf("CORRUPT\n");
        return 0;
    }

    long long r_sum = 0, g_sum = 0, b_sum = 0;
    for (int i = 0; i < 12288; i += 3) {
        r_sum += buf[i];
        g_sum += buf[i+1];
        b_sum += buf[i+2];
    }
    int r_avg = r_sum / 4096;
    int g_avg = g_sum / 4096;
    int b_avg = b_sum / 4096;

    if (r_avg > 200) printf("FAIL\n");
    else if (g_avg > 200) printf("PASS\n");
    else if (b_avg > 200) printf("FLAKY\n");
    else printf("CORRUPT\n");

    return 0;
}
EOF

    gcc -O3 -o /app/oracle_analyzer /app/oracle_analyzer.c
    chmod +x /app/oracle_analyzer

    # Generate a 120-frame video (4 seconds at 30 fps)
    ffmpeg -y -f lavfi -i testsrc=duration=4:size=64x64:rate=30 -c:v libx264 -pix_fmt yuv420p /app/ci_test_run.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user