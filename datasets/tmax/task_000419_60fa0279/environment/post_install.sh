apt-get update && apt-get install -y python3 python3-pip gcc make gawk coreutils
    pip3 install pytest pandas numpy

    mkdir -p /app/vmath-1.2
    mkdir -p /home/user/data

    cat << 'EOF' > /app/vmath-1.2/main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <vec1> <vec2>\n", argv[0]);
        return 1;
    }
    char *v1 = strdup(argv[1]);
    char *v2 = strdup(argv[2]);
    float sum = 0.0;
    char *t1 = strtok(v1, ",");
    char *t2 = strtok(v2, ",");
    while (t1 != NULL && t2 != NULL) {
        float d = atof(t1) - atof(t2);
        sum += d * d;
        t1 = strtok(NULL, ",");
        t2 = strtok(NULL, ",");
    }
    printf("%f\n", sqrt(sum));
    free(v1);
    free(v2);
    return 0;
}
EOF

    cat << 'EOF' > /app/vmath-1.2/Makefile
CC=gcc

all: vmath

vmath: main.c
	$(CC) -o vmath main.c

clean:
	rm -f vmath
EOF

    cat << 'EOF' > /tmp/generate_data.py
import pandas as pd
import numpy as np

np.random.seed(42)

n_hist = 50
X_A = np.random.randn(n_hist, 4) + np.array([0, 0, 0, 0])
X_B = np.random.randn(n_hist, 4) + np.array([5, 5, 5, 5])

hist_df = pd.DataFrame(np.vstack((X_A, X_B)), columns=['feat1', 'feat2', 'feat3', 'feat4'])
hist_df['outcome_class'] = ['A']*n_hist + ['B']*n_hist
hist_df['experiment_id'] = [f'hist_{i}' for i in range(2*n_hist)]
hist_df = hist_df[['experiment_id', 'feat1', 'feat2', 'feat3', 'feat4', 'outcome_class']]
hist_df.to_csv('/home/user/data/historical.csv', index=False)

n_new = 20
X_new_A = np.random.randn(n_new, 4) + np.array([0, 0, 0, 0])
X_new_B = np.random.randn(n_new, 4) + np.array([5, 5, 5, 5])

new_df = pd.DataFrame(np.vstack((X_new_A, X_new_B)), columns=['feat1', 'feat2', 'feat3', 'feat4'])
new_df['true_class'] = ['A']*n_new + ['B']*n_new
new_df['experiment_id'] = [f'new_{i}' for i in range(2*n_new)]

new_df[['experiment_id', 'feat1', 'feat2', 'feat3', 'feat4']].to_csv('/home/user/data/new_experiments.csv', index=False)
new_df[['experiment_id', 'true_class']].to_csv('/app/ground_truth.csv', index=False)
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app