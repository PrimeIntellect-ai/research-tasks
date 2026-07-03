apt-get update && apt-get install -y python3 python3-pip gawk
    pip3 install pytest numpy h5py

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import h5py
import numpy as np
import os

np.random.seed(42)
# Generate 10,000 floating point coverage values (e.g., normal distribution around 50 with some noise)
data = np.random.normal(loc=50.0, scale=15.0, size=10000)
# Add some outliers to make the top 100 interesting
outliers = np.random.uniform(low=100.0, high=150.0, size=50)
data = np.concatenate([data, outliers])
np.random.shuffle(data)

with h5py.File('/home/user/coverage.h5', 'w') as f:
    f.create_dataset('coverage', data=data, dtype='float64')

# Compute the exact expected sum for the top 100
sorted_data = np.sort(data)[::-1]
top_100_sum = np.sum(sorted_data[:100])

with open('/home/user/.expected_sum.txt', 'w') as f:
    f.write(f"{top_100_sum:.4f}\n")
EOF

    python3 /tmp/setup.py

    chmod -R 777 /home/user