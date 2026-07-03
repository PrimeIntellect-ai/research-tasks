apt-get update && apt-get install -y python3 python3-pip gcc ffmpeg
    pip3 install pytest

    mkdir -p /app

    # Generate dummy video with exactly 142 frames
    ffmpeg -f lavfi -i color=c=black:s=320x240:d=5.68 -r 25 /app/dashboard.mp4

    # Create reference implementation
    cat << 'EOF' > /app/ref_process.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char line[256];
    int F = 142;
    int hash[1024];
    for(int i=0; i<1024; i++) hash[i] = -1;

    int last_s1 = -1, last_s2 = -1, last_s3 = -1;

    if (fgets(line, sizeof(line), stdin) == NULL) return 0; // header

    while (fgets(line, sizeof(line), stdin)) {
        int t, s1, s2, s3;
        if (sscanf(line, "%d,%d,%d,%d", &t, &s1, &s2, &s3) != 4) continue;

        int idx = t % 1024;
        if (hash[idx] == t) continue;
        hash[idx] = t;

        if (s1 == -1) s1 = last_s1; else last_s1 = s1;
        if (s2 == -1) s2 = last_s2; else last_s2 = s2;
        if (s3 == -1) s3 = last_s3; else last_s3 = s3;

        int out_s1 = (s1 == -1) ? -1 : s1 ^ F;
        int out_s2 = (s2 == -1) ? -1 : s2 ^ F;
        int out_s3 = (s3 == -1) ? -1 : s3 ^ F;

        printf("%d,s1,%d\n", t, out_s1);
        printf("%d,s2,%d\n", t, out_s2);
        printf("%d,s3,%d\n", t, out_s3);
    }
    return 0;
}
EOF

    # Compile reference implementation
    gcc -O3 /app/ref_process.c -o /app/ref_process

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user