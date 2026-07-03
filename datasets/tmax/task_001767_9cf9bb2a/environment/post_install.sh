apt-get update && apt-get install -y python3 python3-pip curl
    pip3 install pytest

    # Install CPU-only torch to save time and space
    pip3 install torch --index-url https://download.pytorch.org/whl/cpu
    pip3 install sentence-transformers pandas scikit-learn numpy

    mkdir -p /app/bayes-metrics-tracker-1.2.0/bayes_metrics_tracker
    mkdir -p /home/user/data
    mkdir -p /app/reference
    mkdir -p /home/user/artifacts

    # Create vendored package
    cat << 'EOF' > /app/bayes-metrics-tracker-1.2.0/setup.py
from setuptools import setup, find_packages
import os

if os.environ.get("BMT_ENV") != "production":
    raise ValueError("Only production installs allowed")

setup(
    name="bayes-metrics-tracker",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        # missing numpy dependency
    ]
)
EOF

    cat << 'EOF' > /app/bayes-metrics-tracker-1.2.0/bayes_metrics_tracker/__init__.py
from .estimator import CovarianceEstimator
from .logger import Logger
EOF

    cat << 'EOF' > /app/bayes-metrics-tracker-1.2.0/bayes_metrics_tracker/estimator.py
import numpy as np

class CovarianceEstimator:
    def __init__(self, prior_variance=1.0):
        self.prior_variance = prior_variance
        self.cov_matrix = None

    def fit(self, X, y=None):
        n_samples, n_features = X.shape
        emp_cov = np.cov(X, rowvar=False)
        shrinkage = 1.0 / (1.0 + self.prior_variance)
        self.cov_matrix = (1 - shrinkage) * emp_cov + shrinkage * np.eye(n_features)
        return self

    def score(self, X, y=None):
        if self.cov_matrix is None:
            raise ValueError("Not fitted")
        emp_cov = np.cov(X, rowvar=False)
        inv_cov = np.linalg.inv(self.cov_matrix)
        nll = np.trace(np.dot(emp_cov, inv_cov)) + np.linalg.slogdet(self.cov_matrix)[1]
        return -nll

    def get_params(self, deep=True):
        return {"prior_variance": self.prior_variance}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
EOF

    cat << 'EOF' > /app/bayes-metrics-tracker-1.2.0/bayes_metrics_tracker/logger.py
import numpy as np

class Logger:
    @staticmethod
    def save_artifact(cov_matrix, path):
        np.save(path, cov_matrix)
EOF

    # Generate dataset and reference matrix
    python3 -c '
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Generate 150 sentences to allow enough samples for 5-fold CV (30 per fold)
sentences = [f"This is a generated sentence number {i} for testing purposes." for i in range(150)]
sentences += ["The quick brown fox jumps over the lazy dog.", "Artificial intelligence is transforming the world."]

df = pd.DataFrame({"sentence": sentences})
df.to_csv("/home/user/data/sentences.csv", index=False)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(df["sentence"].tolist())
true_cov = np.cov(embeddings, rowvar=False)
np.save("/app/reference/true_cov_matrix.npy", true_cov)
'

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user