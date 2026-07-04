apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest pandas numpy

    mkdir -p /app
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 3) return 1;
    FILE *in = fopen(argv[1], "r");
    FILE *out = fopen(argv[2], "w");
    if (!in || !out) return 1;
    fprintf(out, "id,value\n");
    char line[256];
    if (!fgets(line, sizeof(line), in)) return 1; // skip header
    while (fgets(line, sizeof(line), in)) {
        int id;
        double w, x;
        if (sscanf(line, "%d,%lf,%lf", &id, &w, &x) == 3) {
            double centroid = 0.0;
            double lr = 0.01;
            for (int i = 0; i < 1000; i++) {
                double grad = w * (centroid - x);
                centroid -= lr * grad;
            }
            fprintf(out, "%d,%.8lf\n", id, centroid);
        }
    }
    fclose(in);
    fclose(out);
    return 0;
}
EOF
    gcc -O2 /tmp/oracle.c -o /app/reference_oracle
    strip /app/reference_oracle
    rm /tmp/oracle.c

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/pipeline.py
import pandas as pd
import numpy as np
from multiprocessing.pool import ThreadPool
import sys

def process_row(row):
    id_val = int(row['id'])
    w = np.float32(row['w'])
    x = np.float32(row['x'])
    centroid = np.float32(0.0)
    lr = np.float32(1.5) # Bug: learning rate too high
    for _ in range(1000):
        grad = w * (centroid - x)
        centroid -= lr * grad

    # Bug: non-thread-safe file append
    with open('/home/user/output.csv', 'a') as f:
        f.write(f"{id_val},{centroid}\n")

def main():
    df = pd.read_csv('/home/user/data.csv')
    with open('/home/user/output.csv', 'w') as f:
        f.write("id,value\n")

    pool = ThreadPool(4)
    pool.map(process_row, df.to_dict('records'))
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
EOF

    cat << 'EOF' > /home/user/data.csv
id,w,x
1,0.5,10.0
2,0.8,20.0
3,0.1,5.0
4,0.9,15.0
5,0.3,8.0
6,0.6,12.0
7,0.4,7.0
8,0.7,18.0
9,0.2,3.0
10,0.95,25.0
EOF

    chmod -R 777 /home/user