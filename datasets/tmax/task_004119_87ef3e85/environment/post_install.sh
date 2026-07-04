apt-get update && apt-get install -y python3 python3-pip ffmpeg imagemagick gcc
    pip3 install pytest

    mkdir -p /app

    cat << 'EOF' > /tmp/setup.sh
#!/bin/bash
mkdir -p /app

# Generate sequence
X0=5
X1=12
A=3
B=7
C=14
MOD=101

SEQ=($X0 $X1)
for i in {2..49}; do
    PREV1=${SEQ[$((i-1))]}
    PREV2=${SEQ[$((i-2))]}
    VAL=$(( (A * PREV1 + B * PREV2 + C) % MOD ))
    SEQ+=($VAL)
done

# Create video frames
mkdir -p /tmp/frames
for i in {0..49}; do
    POS=${SEQ[$i]}
    # Create a 100x10 black image, set pixel at (POS, 5) to white
    FRAME_FILE=$(printf "/tmp/frames/frame_%04d.png" $i)
    convert -size 100x10 xc:black -fill white -draw "point $POS,5" $FRAME_FILE
done

# Compile to video
ffmpeg -framerate 10 -i /tmp/frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p /app/experiment.mp4
rm -rf /tmp/frames

# Create the oracle
cat << 'ORACLE_EOF' > /app/oracle_predictor.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 4) return 1;
    long long x0 = atoll(argv[1]);
    long long x1 = atoll(argv[2]);
    long long N = atoll(argv[3]);

    long long a = 3, b = 7, c = 14, mod = 101;

    if (N == 0) { printf("%lld\n", x0); return 0; }
    if (N == 1) { printf("%lld\n", x1); return 0; }

    long long prev2 = x0;
    long long prev1 = x1;
    long long curr = 0;

    for (long long i = 2; i <= N; i++) {
        curr = (a * prev1 + b * prev2 + c) % mod;
        if (curr < 0) curr += mod; // Handle negative modulo just in case
        prev2 = prev1;
        prev1 = curr;
    }

    printf("%lld\n", curr);
    return 0;
}
ORACLE_EOF

gcc -O3 /app/oracle_predictor.c -o /app/oracle_predictor
chmod +x /app/oracle_predictor
EOF

    bash /tmp/setup.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user