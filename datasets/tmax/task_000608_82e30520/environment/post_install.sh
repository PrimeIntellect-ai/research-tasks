apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Generate a dummy spectroscopy video
    ffmpeg -f lavfi -i "color=c=black:s=100x100:d=2" -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{n}':fontcolor=white:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2" -c:v libx264 -y /app/spectroscopy_run.mp4

    # Generate a dummy PDB file
    cat << 'EOF' > /app/target.pdb
HEADER    DUMMY PROTEIN
ATOM      1  N   ALA A   1      11.104   6.134  -6.504  1.00  0.00           N  
ATOM      2  CA  ALA A   1      11.639   6.071  -5.147  1.00  0.00           C  
HETATM    3  O   HOH A 201      12.639   5.071  -5.147  1.00  0.00           O
HETATM    4  O   HOH A 202      10.639   7.071  -4.147  1.00  0.00           O
HETATM    5  O   HOH A 203      11.639   8.071  -6.147  1.00  0.00           O
EOF

    # Compile the Oracle C program
    cat << 'EOF' > /tmp/oracle_mc_sim.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    if (argc != 3) return 1;
    char *seq = argv[1];
    int K = atoi(argv[2]);
    int len = strlen(seq);
    int N = len * K;

    uint64_t X = K;
    for (int i = 0; i < len; i++) {
        X += seq[i];
    }

    int collisions = 0;
    uint64_t m = 1ULL << 31;

    for (int i = 0; i < N; i++) {
        X = (1103515245ULL * X + 12345ULL) % m;
        double x_coord = (double)X / m;

        X = (1103515245ULL * X + 12345ULL) % m;
        double y_coord = (double)X / m;

        if (x_coord * x_coord + y_coord * y_coord <= 1.0) {
            collisions++;
        }
    }

    printf("%d\n", collisions);
    return 0;
}
EOF
    gcc -O3 /tmp/oracle_mc_sim.c -o /app/oracle_mc_sim
    chmod +x /app/oracle_mc_sim

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user