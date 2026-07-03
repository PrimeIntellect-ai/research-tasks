apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy scipy pandas scikit-learn papermill jupyter

    mkdir -p /home/user/data

    cat << 'EOF' > /tmp/setup.py
import os
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

# Setup directories
data_dir = "/home/user/data"
os.makedirs(data_dir, exist_ok=True)

# 1. Generate particles.csv
np.random.seed(42)
n_samples = 1000
x = np.random.normal(loc=0, scale=1, size=n_samples)
y = np.random.normal(loc=1, scale=0.5, size=n_samples)
z = np.random.normal(loc=-1, scale=2, size=n_samples)

df = pd.DataFrame({'x': x, 'y': y, 'z': z})
df.to_csv(os.path.join(data_dir, "particles.csv"), index=False)

# 2. Generate Grid
grid_x, grid_y = np.mgrid[-3:3:50j, -2:4:50j]
np.save(os.path.join(data_dir, "grid_X.npy"), grid_x)
np.save(os.path.join(data_dir, "grid_Y.npy"), grid_y)

# 3. Generate reference density
positions = np.vstack([grid_x.ravel(), grid_y.ravel()])
values = np.vstack([x, y])
kernel_ref = gaussian_kde(values, bw_method=0.20)
f_ref = np.reshape(kernel_ref(positions).T, grid_x.shape)
np.save(os.path.join(data_dir, "reference_density.npy"), f_ref)

# Compute expected MAD for testing verification
kernel_agent = gaussian_kde(values, bw_method=0.25)
f_agent = np.reshape(kernel_agent(positions).T, grid_x.shape)
f_agent_64 = f_agent.astype(np.float64)
f_ref_64 = f_ref.astype(np.float64)
expected_mad = np.max(np.abs(f_agent_64 - f_ref_64))

with open(os.path.join(data_dir, "expected_mad.txt"), "w") as f:
    f.write(f"{expected_mad:.6f}")
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user