apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy scikit-learn

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import numpy as np

# Set seed for generation
np.random.seed(42)

# Generate 950 "normal" samples clustered in 5 groups
data = []
for i in range(5):
    cluster_data = np.random.normal(loc=i*2, scale=1.0, size=(190, 50))
    data.append(cluster_data)
data = np.vstack(data)

# Generate 50 extreme outliers
outliers = np.random.normal(loc=20, scale=5.0, size=(50, 50))

# Combine and shuffle
all_data = np.vstack([data, outliers])
shuffle_idx = np.random.permutation(1000)
shuffled_data = all_data[shuffle_idx]

# Save true outlier indices for our reference (the agent needs to find these)
true_outliers = np.sort(np.where(shuffle_idx >= 950)[0])

np.save('/home/user/raw_embeddings.npy', shuffled_data)
np.save('/home/user/.true_outliers.npy', true_outliers)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user