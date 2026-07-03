apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy matplotlib scikit-learn

    mkdir -p /app/custom_vec_eval-1.0.0/custom_vec_eval
    mkdir -p /home/user

    cat << 'EOF' > /app/custom_vec_eval-1.0.0/setup.py
from setuptools import setup, find_packages
setup(
    name='custom_vec_eval',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib']
)
EOF

    cat << 'EOF' > /app/custom_vec_eval-1.0.0/custom_vec_eval/__init__.py
from .metrics import recall_at_k
from .plot import plot_recall
EOF

    cat << 'EOF' > /app/custom_vec_eval-1.0.0/custom_vec_eval/metrics.py
import numpy as np

def get_top_k(queries, embeddings, k=10):
    dist = np.sum(queries**2, axis=1)[:, np.newaxis] + np.sum(embeddings**2, axis=1) + 2 * np.dot(queries, embeddings.T)
    return np.argsort(dist, axis=1)[:, :k]

def recall_at_k(queries, embeddings, ground_truth, k=10):
    top_k = get_top_k(queries, embeddings, k)
    hits = [1 if gt in top_k[i] else 0 for i, gt in enumerate(ground_truth)]
    return np.mean(hits)
EOF

    cat << 'EOF' > /app/custom_vec_eval-1.0.0/custom_vec_eval/plot.py
import matplotlib
matplotlib.use('Template')
import matplotlib.pyplot as plt

def plot_recall(recall_val, save_path):
    plt.figure()
    plt.bar(['Recall@10'], [recall_val])
    plt.savefig(save_path)
EOF

    cat << 'EOF' > /tmp/generate_data.py
import os
import numpy as np

np.random.seed(42)
embeddings = np.random.randn(1000, 50)
ground_truth = np.random.choice(1000, 100, replace=False)
true_queries = embeddings[ground_truth] + np.random.randn(100, 50) * 0.1

# Apply hidden transformation W, b
W = np.random.randn(50, 50) * 0.5
b = np.random.randn(50) * 2.0
queries_raw = true_queries @ np.linalg.inv(W) - b @ np.linalg.inv(W)

np.save('/home/user/embeddings.npy', embeddings)
np.save('/home/user/queries_raw.npy', queries_raw)
np.save('/home/user/ground_truth.npy', ground_truth)
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user