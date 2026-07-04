# test_final_state.py

import os
import json
import subprocess
import sys
import pytest

def test_json_output_exists():
    """Verify that the output JSON file was created."""
    assert os.path.exists("/home/user/best_model.json"), "Output file /home/user/best_model.json does not exist."

def test_json_output_format():
    """Verify that the JSON file has the correct structure."""
    with open("/home/user/best_model.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("File /home/user/best_model.json is not valid JSON.")

    assert "best_alpha" in data, "Missing 'best_alpha' in JSON."
    assert "cv_mse" in data, "Missing 'cv_mse' in JSON."
    assert isinstance(data["best_alpha"], (int, float)), "'best_alpha' must be a number."
    assert isinstance(data["cv_mse"], (int, float)), "'cv_mse' must be a number."
    assert data["cv_mse"] > 0, "'cv_mse' must be positive."

def test_correct_values():
    """Verify that the computed best_alpha and cv_mse match the ground truth."""
    # We dynamically compute the ground truth using the agent's environment
    # to strictly adhere to the standard library constraint in the test file itself.
    script = """
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

class GroundTruthPCA(BaseEstimator, TransformerMixin):
    def __init__(self, n_components=3):
        self.n_components = n_components

    def fit(self, X, y=None):
        cov_mat = np.cov(X, rowvar=False)
        eigen_vals, eigen_vecs = np.linalg.eigh(cov_mat)
        sorted_indices = np.argsort(eigen_vals)[::-1]
        self.components_ = eigen_vecs[:, sorted_indices[:self.n_components]]
        return self

    def transform(self, X):
        return np.dot(X, self.components_)

df = pd.read_csv("/home/user/dataset.csv")
X = df.drop(columns=['target']).values
y = df['target'].values

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', GroundTruthPCA(n_components=3)),
    ('ridge', Ridge())
])

param_grid = {'ridge__alpha': [0.1, 1.0, 10.0]}
cv = KFold(n_splits=5, shuffle=True, random_state=42)

grid = GridSearchCV(pipeline, param_grid, cv=cv, scoring='neg_mean_squared_error')
grid.fit(X, y)

best_alpha = grid.best_params_['ridge__alpha']
cv_mse = -grid.best_score_

with open("/tmp/truth.json", "w") as f:
    json.dump({"best_alpha": best_alpha, "cv_mse": cv_mse}, f)
"""
    script_path = "/tmp/compute_truth.py"
    with open(script_path, "w") as f:
        f.write(script)

    try:
        subprocess.check_call([sys.executable, script_path])
    except subprocess.CalledProcessError:
        pytest.fail("Failed to compute ground truth. Ensure numpy, pandas, and scikit-learn are installed in the environment.")

    with open("/tmp/truth.json", "r") as f:
        truth = json.load(f)

    with open("/home/user/best_model.json", "r") as f:
        agent_data = json.load(f)

    assert agent_data["best_alpha"] == truth["best_alpha"], f"Alpha mismatch: Expected {truth['best_alpha']}, got {agent_data['best_alpha']}"

    # Check MSE with a small relative tolerance
    diff = abs(agent_data["cv_mse"] - truth["cv_mse"])
    assert diff / truth["cv_mse"] < 1e-3, f"MSE mismatch: Expected {truth['cv_mse']}, got {agent_data['cv_mse']}"