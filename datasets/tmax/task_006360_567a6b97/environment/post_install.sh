apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest h5py numpy

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import h5py
import numpy as np

def setup():
    data = np.array([2, 3, 1, 4, 2, 5, 2, 3, 1, 2, 4, 3, 2, 1, 3, 2, 4, 1, 3, 2], dtype=np.int32)
    with h5py.File('/home/user/mutation_counts.h5', 'w') as f:
        f.create_dataset('counts', data=data)

setup()
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user