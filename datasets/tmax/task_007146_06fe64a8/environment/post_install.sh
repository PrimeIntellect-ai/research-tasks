apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas numpy

    mkdir -p /home/user

    cat << 'EOF' > /tmp/setup_and_solve.py
import pandas as pd
import numpy as np
import json
import os

# 1. Generate sequences.csv
np.random.seed(123)
dates = pd.date_range(start='2023-01-01', periods=5, freq='D')
batches = ['B1', 'B2', 'B3', 'B4', 'B5']

# Create a periodic signal mixed with noise
# Base pattern: ATGC (length 4) -> repeats
base_pattern = "ATGC" * 50 # length 200
# Add some random noise
mapping_rev = {1: 'A', 2: 'C', 3: 'G', 4: 'T'}
noise = "".join([mapping_rev[np.random.randint(1, 5)] for _ in range(50)])
full_seq = base_pattern + noise + base_pattern + noise

# split into 5 chunks randomly (but keep order)
chunks = [full_seq[i:i+100] for i in range(0, 500, 100)]

# shuffle the rows for the CSV so the agent HAS to sort them
df = pd.DataFrame({
    'batch_id': batches,
    'recorded_at': dates,
    'sequence': chunks
})
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
df_shuffled.to_csv('/home/user/sequences.csv', index=False)

# 2. Compute Ground Truth
# Sort and concat
df_sorted = df_shuffled.sort_values('recorded_at')
combined_seq = "".join(df_sorted['sequence'].values)

# Map
mapping = {'A': 1, 'C': 2, 'G': 3, 'T': 4}
num_array = np.array([mapping[char] for char in combined_seq])

# FFT
psd = np.abs(np.fft.fft(num_array))**2
psd_no_dc = psd[1:]
max_idx = int(np.argmax(psd_no_dc) + 1)
max_val = round(float(np.max(psd_no_dc)), 2)

# Monte Carlo
np.random.seed(42)
mc_max_vals = []
for _ in range(1000):
    shuffled = np.random.permutation(num_array)
    shuffled_psd = np.abs(np.fft.fft(shuffled))**2
    mc_max_vals.append(np.max(shuffled_psd[1:]))

threshold = round(float(np.percentile(mc_max_vals, 95)), 2)

# Output exact expected values to a hidden file for test verification
expected = {
    "max_psd_index": max_idx,
    "max_psd_value": max_val,
    "mc_threshold_95": threshold
}

with open('/tmp/expected_output.json', 'w') as f:
    json.dump(expected, f)
EOF

    python3 /tmp/setup_and_solve.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user