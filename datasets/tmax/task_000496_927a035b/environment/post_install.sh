apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest numpy pandas scipy emcee

mkdir -p /home/user/data

cat << 'EOF' > /home/user/data/genome.fasta
>synthetic_genome_v1
CGCAGCTAGCTACGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAT
CGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAT
CGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAT
ATGCGTACGTTAGCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGA
EOF

cat << 'EOF' > /tmp/generate_data.py
import numpy as np
import pandas as pd

np.random.seed(123)
times = np.linspace(0, 20, 21)
k_prod_true = 2.5
k_deg_true = 0.4
# Analytical solution: p(t) = (k_prod/k_deg) * (1 - exp(-k_deg * t))
p_true = (k_prod_true / k_deg_true) * (1 - np.exp(-k_deg_true * times))
# Add noise sigma = 0.5
p_obs = p_true + np.random.normal(0, 0.5, size=len(times))

df = pd.DataFrame({'time': times, 'protein': p_obs})
df.to_csv('/home/user/data/expression_data.csv', index=False)
EOF

python3 /tmp/generate_data.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user