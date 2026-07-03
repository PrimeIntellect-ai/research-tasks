apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy scipy h5py netCDF4

    mkdir -p /home/user/data
    mkdir -p /home/user/results

    cat << 'EOF' > /tmp/generate_data.py
import h5py
import numpy as np

np.random.seed(42)
N = 50
x0 = np.random.uniform(1.0, 2.0, N)
y0 = np.random.uniform(-1.0, -0.5, N)
alpha = np.random.uniform(0.1, 0.5, N)

with h5py.File('/home/user/data/initial_conditions.h5', 'w') as f:
    f.create_dataset('x0', data=x0)
    f.create_dataset('y0', data=y0)
    f.create_dataset('alpha', data=alpha)
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user