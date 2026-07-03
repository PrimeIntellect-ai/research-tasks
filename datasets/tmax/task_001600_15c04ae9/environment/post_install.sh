apt-get update && apt-get install -y python3 python3-pip gcc
pip3 install pytest numpy

useradd -m -s /bin/bash user || true

cat << 'EOF' > /tmp/setup.py
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

dim = 64
num_base = 1000
num_query = 50

# Generate random normal arrays
base = np.random.randn(num_base, dim).astype(np.float32)
query = np.random.randn(num_query, dim).astype(np.float32)

# Write to binary files
base.tofile('/home/user/base_embeddings.bin')
query.tofile('/home/user/query_embeddings.bin')

# Compute expected ground truth
base_norm = base / np.linalg.norm(base, axis=1, keepdims=True)
query_norm = query / np.linalg.norm(query, axis=1, keepdims=True)
sims = query_norm @ base_norm.T

best_idx = np.argmax(sims, axis=1)
best_sims = np.max(sims, axis=1)

with open('/home/user/expected_neighbors.csv', 'w') as f:
    f.write("query_id,nearest_base_id,cosine_similarity\n")
    for i in range(num_query):
        f.write(f"{i},{best_idx[i]},{best_sims[i]:.4f}\n")
EOF

python3 /tmp/setup.py
rm /tmp/setup.py

chmod -R 777 /home/user