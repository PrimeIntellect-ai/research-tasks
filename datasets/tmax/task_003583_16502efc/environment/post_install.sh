apt-get update && apt-get install -y python3 python3-pip gcc
pip3 install pytest pandas scikit-learn numpy

# Create the embedder_oracle binary
mkdir -p /app
cat << 'EOF' > /app/embedder_oracle.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    int id = atoi(argv[1]);
    srand(id);
    for (int i = 0; i < 128; i++) {
        float val = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
        printf("%f%s", val, i == 127 ? "" : ",");
    }
    printf("\n");
    return 0;
}
EOF

gcc -O2 /app/embedder_oracle.c -o /app/embedder_oracle
strip /app/embedder_oracle
rm /app/embedder_oracle.c

# Generate the corrupted dataset
mkdir -p /home/user
cat << 'EOF' > /tmp/generate_data.py
import pandas as pd
import numpy as np
import subprocess

np.random.seed(42)
ids = np.arange(1000, 2000)
data = []

for cid in ids:
    res = subprocess.run(['/app/embedder_oracle', str(cid)], capture_output=True, text=True)
    vec = [float(x) for x in res.stdout.strip().split(',')]
    data.append([float(cid)] + vec)

df = pd.DataFrame(data, columns=['concept_id'] + [f'dim_{i}' for i in range(128)])

# 2% concept_id = NaN, embeddings = NaN
idx_nan_id = np.random.choice(df.index, size=int(0.02 * len(df)), replace=False)
df.loc[idx_nan_id, 'concept_id'] = np.nan
df.loc[idx_nan_id, [f'dim_{i}' for i in range(128)]] = np.nan

# 10% embeddings = NaN (concept_id remains valid float)
remaining_idx = df.index.difference(idx_nan_id)
idx_nan_emb = np.random.choice(remaining_idx, size=int(0.10 * len(df)), replace=False)
df.loc[idx_nan_emb, [f'dim_{i}' for i in range(128)]] = np.nan

df.to_csv('/home/user/corrupted_data.csv', index=False)
EOF

python3 /tmp/generate_data.py
rm /tmp/generate_data.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user