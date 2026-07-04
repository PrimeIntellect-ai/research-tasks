apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest pandas scikit-learn

    mkdir -p /app/vendored/window_agg/
    mkdir -p /app/data/logs/

    cat << 'EOF' > /app/vendored/window_agg/agg.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    long window = atol(argv[1]);
    long ts;
    int status;
    long current_window = -1;
    long count = 0;

    while (scanf("%ld,%d", &ts, &status) == 2) {
        long w = floor((double)ts / window) * window;
        if (current_window == -1) current_window = w;

        if (w != current_window) {
            printf("%ld,%ld\n", current_window, count);
            current_window = w;
            count = 0;
        }
        if (status == 404) {
            count++;
        }
    }
    if (current_window != -1) {
        printf("%ld,%ld\n", current_window, count);
    }
    return 0;
}
EOF

    # Creating Makefile with exactly 8 spaces instead of a tab, and missing -lm
    printf "all: agg.c\n        gcc -O3 -o window_agg agg.c\n" > /app/vendored/window_agg/Makefile

    cat << 'EOF' > /tmp/gen_logs.py
import random
from datetime import datetime, timedelta

start = datetime(2023, 10, 1, 10, 0, 0)
logs_utf8 = []
logs_utf16 = []
logs_iso = []

truth_counts = {}

for i in range(1000):
    ts = start + timedelta(seconds=random.randint(0, 3600))
    status = random.choice([200, 200, 200, 404, 500])

    if status == 404:
        w = (int(ts.timestamp()) // 300) * 300
        truth_counts[w] = truth_counts.get(w, 0) + 1

    if i % 3 == 0:
        logs_utf8.append(f'{ts.strftime("%Y-%m-%d %H:%M:%S")} INFO {status} /page\n')
    elif i % 3 == 1:
        logs_utf16.append(f'{ts.strftime("%d/%b/%Y:%H:%M:%S")} WARN {status} /page\n')
    else:
        logs_iso.append(f'{ts.strftime("%Y-%m-%d %H:%M:%S")} DEBUG {status} /page\n')

with open('/app/data/logs/server1.log', 'w', encoding='utf-8') as f: f.writelines(logs_utf8)
with open('/app/data/logs/server2.log', 'w', encoding='utf-16le') as f: f.writelines(logs_utf16)
with open('/app/data/logs/server3.log', 'w', encoding='iso-8859-1') as f: f.writelines(logs_iso)

with open('/app/ground_truth.csv', 'w') as f:
    for w in sorted(truth_counts.keys()):
        f.write(f'{w},{truth_counts[w]}\n')
EOF

    python3 /tmp/gen_logs.py
    rm /tmp/gen_logs.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user