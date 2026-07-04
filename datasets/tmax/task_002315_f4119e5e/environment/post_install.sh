apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy pandas scikit-learn

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/data/metrics

    cat << 'EOF' > /tmp/setup.py
import os
import json
import numpy as np
import pandas as pd

np.random.seed(42)
os.makedirs("/home/user/data/metrics", exist_ok=True)

n_train = 80
n_test = 20
total = n_train + n_test

exp_ids = [f"exp_{i:03d}" for i in range(total)]
np.random.shuffle(exp_ids)
train_ids = exp_ids[:n_train]
test_ids = exp_ids[n_train:]

dataset_sizes = np.random.randint(1000, 10000, total)
batch_sizes = np.random.choice([16, 32, 64, 128], total)
optimizers = np.random.choice(['adam', 'sgd', 'rmsprop'], total)
lrs = np.random.uniform(0.0001, 0.1, total)

# Generate synthetic loss curves (10 epochs)
loss_base = np.linspace(2.0, 0.5, 10)
curves = []
for i in range(total):
    noise = np.random.normal(0, 0.1, 10)
    decay = np.exp(-np.linspace(0, 3, 10) * lrs[i] * 100)
    curve = loss_base * decay + noise
    curves.append(curve.tolist())

# Generate final accuracy
final_accs = 0.95 - 0.1 * curves[-1][-1] + 0.05 * (dataset_sizes / 10000) - 0.02 * (batch_sizes / 128) + np.random.normal(0, 0.02, total)
final_accs = np.clip(final_accs, 0, 1)

# Write CSVs
train_df = pd.DataFrame({'exp_id': train_ids})
test_df = pd.DataFrame({'exp_id': test_ids})

all_df = pd.DataFrame({
    'exp_id': exp_ids,
    'dataset_size': dataset_sizes,
    'batch_size': batch_sizes,
    'optimizer': optimizers
})

train_df = pd.merge(train_df, all_df, on='exp_id')
test_df = pd.merge(test_df, all_df, on='exp_id')

train_df.to_csv("/home/user/data/train_metadata.csv", index=False)
test_df.to_csv("/home/user/data/test_metadata.csv", index=False)

# Write JSONs
for i, eid in enumerate(exp_ids):
    data = {
        "learning_rate": lrs[i],
        "val_loss_curve": curves[i]
    }
    if eid in train_ids:
        data["final_val_accuracy"] = float(final_accs[i])

    with open(f"/home/user/data/metrics/{eid}.json", "w") as f:
        json.dump(data, f)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user