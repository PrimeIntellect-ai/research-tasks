apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy pandas scipy

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup_data.py
import numpy as np
import pandas as pd
import os

np.random.seed(123)
ref_data = np.concatenate([np.random.normal(0, 1, 700), np.random.normal(4, 1.5, 300)])
batch_data = np.concatenate([np.random.normal(0.5, 1.2, 350), np.random.normal(4.5, 1.6, 150)])

os.makedirs('/home/user', exist_ok=True)
pd.DataFrame({'value': ref_data}).to_csv('/home/user/reference.csv', index=False)
pd.DataFrame({'value': batch_data}).to_csv('/home/user/batch.csv', index=False)
EOF

    python3 /tmp/setup_data.py
    rm /tmp/setup_data.py

    chmod -R 777 /home/user