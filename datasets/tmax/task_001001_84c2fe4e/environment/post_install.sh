apt-get update && apt-get install -y python3 python3-pip g++ wget
    pip3 install pytest pandas scikit-learn numpy

    # Vendor rapidcsv
    mkdir -p /app/rapidcsv/src
    wget https://raw.githubusercontent.com/d99kris/rapidcsv/master/src/rapidcsv.h -O /app/rapidcsv/src/rapidcsv.h

    # Perturb the rapidcsv header
    sed -i "s/explicit SeparatorParams(const char pSeparator = ',',/explicit SeparatorParams(const char pSeparator = '|',/" /app/rapidcsv/src/rapidcsv.h

    # Create user
    useradd -m -s /bin/bash user || true

    # Generate synthetic data
    cat << 'EOF' > /tmp/generate_data.py
import pandas as pd
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=1000, n_features=5, n_informative=3, n_redundant=0, random_state=42, class_sep=2.0)
user_ids = np.arange(1000)

features = pd.DataFrame(X, columns=[f'f{i}' for i in range(5)])
features['user_id'] = user_ids
labels = pd.DataFrame({'user_id': user_ids, 'label': y})

# split train/test
np.random.seed(42)
train_idx = np.random.rand(1000) < 0.8
features_train = features[train_idx]
labels_train = labels[train_idx]
features_test = features[~train_idx]
labels_test = labels[~train_idx]

features_train.to_csv('/home/user/features.csv', index=False)
labels_train.to_csv('/home/user/labels.csv', index=False)
features_test.drop(columns=['label'], errors='ignore').to_csv('/home/user/test_features.csv', index=False)
labels_test[['user_id', 'label']].to_csv('/tmp/hidden_test_labels.csv', index=False)
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    chmod -R 777 /home/user