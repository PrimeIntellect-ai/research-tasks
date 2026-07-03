apt-get update && apt-get install -y python3 python3-pip gcc gawk sed coreutils bash
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/calc_sim.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int levenshtein(const char *s1, const char *s2) {
    int len1 = strlen(s1), len2 = strlen(s2);
    int *column = malloc((len1 + 1) * sizeof(int));
    for (int y = 1; y <= len1; y++) column[y] = y;
    for (int x = 1; x <= len2; x++) {
        column[0] = x;
        for (int y = 1, lastdiag = x - 1; y <= len1; y++) {
            int olddiag = column[y];
            column[y] = s1[y-1] == s2[x-1] ? lastdiag :
                        (column[y] < column[y-1] ? 
                         (column[y] < lastdiag ? column[y] : lastdiag) :
                         (column[y-1] < lastdiag ? column[y-1] : lastdiag)) + 1;
            lastdiag = olddiag;
        }
    }
    int res = column[len1];
    free(column);
    return res;
}

int main(int argc, char **argv) {
    if (argc < 3) return 1;
    int dist = levenshtein(argv[1], argv[2]);
    int maxlen = strlen(argv[1]) > strlen(argv[2]) ? strlen(argv[1]) : strlen(argv[2]);
    double sim = maxlen == 0 ? 1.0 : 1.0 - ((double)dist / maxlen);
    printf("%.4f\n", sim);
    return 0;
}
EOF
    gcc -O3 -o /app/calc_sim /app/calc_sim.c
    strip /app/calc_sim
    rm /app/calc_sim.c

    mkdir -p /home/user/corpora/clean
    mkdir -p /home/user/corpora/evil
    mkdir -p /home/user/corpora/golden_evil

    python3 -c "
import os

def generate_data():
    for i in range(5):
        with open(f'/home/user/corpora/clean/clean_{i}.csv', 'w') as f:
            f.write('DeviceID,Timestamp,Payload\n')
            for j in range(50):
                f.write(f'DEV{j%5},{1600000000 + j*20},PAYLOAD_CLEAN_{j}\n')

    for i in range(5):
        with open(f'/home/user/corpora/evil/evil_{i}.csv', 'w') as f_evil, \
             open(f'/home/user/corpora/golden_evil/evil_{i}.csv', 'w') as f_gold:
            f_evil.write('DeviceID,Timestamp,Payload\n')
            f_gold.write('DeviceID,Timestamp,Payload\n')
            for j in range(100):
                ts = 1600000000 + j*20
                payload = f'PAYLOAD_EVIL_{j}ABCDEFGH'
                f_evil.write(f'DEV{j%5},{ts},{payload}\n')
                f_gold.write(f'DEV{j%5},{ts},{payload}\n')
                if j % 10 == 0:
                    f_evil.write(f'DEV{j%5},{ts+5},{payload}X\n')

generate_data()
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user