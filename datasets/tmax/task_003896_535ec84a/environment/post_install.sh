apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    mkdir -p /home/user/src

    cat << 'EOF' > /home/user/target.txt
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCGGGAAATTTCCCGGGAATTTCGATCGATCGATCGATCGATC
EOF

    cat << 'EOF' > /home/user/src/scoring.c
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 3) return 1;
    char *primer = argv[1];
    char *target = argv[2];
    int plen = strlen(primer);
    int tlen = strlen(target);
    int max_score = 0;

    for (int i = 0; i <= tlen - plen; i++) {
        int score = 0;
        for (int j = 0; j < plen; j++) {
            if (primer[j] == target[i+j]) score++;
        }
        if (score > max_score) max_score = score;
    }
    printf("%d\n", max_score);
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user