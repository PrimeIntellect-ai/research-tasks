apt-get update && apt-get install -y python3 python3-pip curl tar
    pip3 install pytest numpy pandas scikit-learn setuptools setuptools_scm

    mkdir -p /home/user/data
    mkdir -p /app

    # Download and extract emcee 3.1.4
    curl -sL https://github.com/dfm/emcee/archive/refs/tags/v3.1.4.tar.gz | tar -xz -C /app/

    # Inject perturbation into setup.py
    sed -i '15i \    raise RuntimeError("Oops, the researcher broke the setup script!")' /app/emcee-3.1.4/setup.py

    # Generate Synthetic Data
    cat << 'EOF' > /tmp/gen_data.py
import numpy as np
import pandas as pd
from sklearn.datasets import make_regression

np.random.seed(42)
X, y = make_regression(n_samples=1500, n_features=50, n_informative=10, noise=1.0, random_state=42)

# Create a clear 3-factor structure to reward PCA
W = np.random.randn(50, 3)
factors = np.random.randn(1500, 3)
X = factors @ W.T + np.random.randn(1500, 50) * 0.5
y = 2.5 * factors[:, 0] - 1.2 * factors[:, 1] + 3.4 * factors[:, 2] + np.random.randn(1500) * 1.0

# Split
X_train, y_train = X[:1000], y[:1000]
X_test, y_test = X[1000:], y[1000:]

cols = [f"f{i}" for i in range(50)]

train_df = pd.DataFrame(X_train, columns=cols)
train_df['target'] = y_train
train_df.to_csv('/home/user/data/train.csv', index=False)

test_df = pd.DataFrame(X_test, columns=cols)
test_df.to_csv('/home/user/data/test.csv', index=False)

# Hidden true targets
np.savetxt('/home/user/data/test_targets_hidden.csv', y_test)
EOF

    python3 /tmp/gen_data.py
    rm /tmp/gen_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app/emcee-3.1.4