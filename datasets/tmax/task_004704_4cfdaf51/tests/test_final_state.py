# test_final_state.py

import os
import json
import math
import sys
import subprocess
import pytest

def get_expected_metrics():
    """
    Computes the expected metrics by running the exact procedure in a subprocess.
    This allows us to use the container's installed data science libraries while
    keeping the test file strictly using the Python standard library.
    """
    script = """
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

df = pd.read_csv('/home/user/data/dataset.csv')
X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

class CorrelationSelector(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=0.85):
        self.threshold = threshold
        self.drop_cols = []

    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            corr = X.corr().abs()
            upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
            self.drop_cols = [column for column in upper.columns if any(upper[column] > self.threshold)]
        return self

    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            return X.drop(columns=self.drop_cols)
        # Fallback for numpy arrays if needed
        return X

mses = []
for i in range(100):
    X_boot = X_train.sample(frac=1.0, replace=True, random_state=i)
    y_boot = y_train.loc[X_boot.index]

    pipe = Pipeline([
        ('corr', CorrelationSelector()),
        ('scaler', StandardScaler()),
        ('ridge', Ridge())
    ])
    pipe.fit(X_boot, y_boot)
    preds = pipe.predict(X_test)
    mses.append(mean_squared_error(y_test, preds))

import json
print(json.dumps({
    "mean_mse": float(np.mean(mses)),
    "ci_lower": float(np.percentile(mses, 2.5)),
    "ci_upper": float(np.percentile(mses, 97.5))
}))
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Failed to compute expected metrics. Error: {result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse expected metrics JSON. Output: {result.stdout}")

def test_artifacts_exist():
    metrics_path = "/home/user/artifacts/metrics.json"
    pipeline_path = "/home/user/artifacts/pipeline.pkl"

    assert os.path.isfile(metrics_path), f"Metrics file missing at {metrics_path}"
    assert os.path.isfile(pipeline_path), f"Pipeline artifact missing at {pipeline_path}"

def test_metrics_format_and_values():
    metrics_path = "/home/user/artifacts/metrics.json"

    with open(metrics_path, "r") as f:
        try:
            student_metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} is not valid JSON.")

    required_keys = {"mean_mse", "ci_lower", "ci_upper"}
    assert required_keys.issubset(student_metrics.keys()), \
        f"Metrics JSON must contain keys {required_keys}. Found: {list(student_metrics.keys())}"

    expected_metrics = get_expected_metrics()

    for key in required_keys:
        student_val = student_metrics[key]
        expected_val = expected_metrics[key]

        assert isinstance(student_val, (int, float)), f"Value for {key} must be a number."

        # Check within 1% tolerance
        tolerance = 0.01 * expected_val
        assert math.isclose(student_val, expected_val, abs_tol=tolerance), \
            f"Value for {key} ({student_val}) is not within 1% of expected ({expected_val}). " \
            "Check that you dropped highly correlated features (f3), fixed the data leak, and used the correct bootstrap seeds."