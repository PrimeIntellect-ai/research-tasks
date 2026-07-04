# test_final_state.py

import os
import json
import pytest
import subprocess
import sys

def get_expected_metrics():
    """
    Computes the expected metrics using the canonical solution.
    We run this in a subprocess to strictly adhere to the rule of using only standard 
    library imports in the test file itself, while leveraging the environment's packages.
    """
    script = """
import pandas as pd
import numpy as np
import json
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df = pd.read_csv('/home/user/data/sensor_readings.csv')
sensor_cols = ['s1', 's2', 's3', 's4', 's5']

# 1. Impute median
for col in sensor_cols:
    df[col] = df[col].fillna(df[col].median())

# 2. Clip at 5th and 95th percentiles
for col in sensor_cols:
    lower = df[col].quantile(0.05)
    upper = df[col].quantile(0.95)
    df[col] = df[col].clip(lower=lower, upper=upper)

# 3. Feature engineering
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour

# 4. PCA
pca = PCA(n_components=2, svd_solver='full')
pca_features = pca.fit_transform(df[sensor_cols])
df['pca1'] = pca_features[:, 0]
df['pca2'] = pca_features[:, 1]

# 5. Model Training
X = df[['hour', 'pca1', 'pca2']]
y = df['target']
model = LinearRegression()
model.fit(X, y)
preds = model.predict(X)

# 6. Evaluation & Bootstrapping
mse = mean_squared_error(y, preds)

np.random.seed(42)
n = len(df)
bootstrap_mses = []
y_arr = y.values
preds_arr = preds

for _ in range(1000):
    indices = np.random.choice(n, n, replace=True)
    b_y = y_arr[indices]
    b_preds = preds_arr[indices]
    bootstrap_mses.append(mean_squared_error(b_y, b_preds))

ci_lower = np.percentile(bootstrap_mses, 2.5)
ci_upper = np.percentile(bootstrap_mses, 97.5)

expected = {
    "mse": mse,
    "mse_ci_lower": ci_lower,
    "mse_ci_upper": ci_upper
}
print(json.dumps(expected))
"""
    try:
        result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected metrics. Subprocess error: {e.stderr}")

def test_metrics_json_exists():
    assert os.path.exists('/home/user/metrics.json'), "/home/user/metrics.json does not exist. The script must output the results to this exact path."
    assert os.path.isfile('/home/user/metrics.json'), "/home/user/metrics.json exists but is not a file."

def test_metrics_values():
    metrics_path = '/home/user/metrics.json'
    assert os.path.exists(metrics_path), "Cannot validate values because /home/user/metrics.json is missing."

    with open(metrics_path, 'r') as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/metrics.json is not valid JSON.")

    expected = get_expected_metrics()

    required_keys = ["mse", "mse_ci_lower", "mse_ci_upper"]
    for key in required_keys:
        assert key in actual, f"Key '{key}' is missing from the JSON output."

        act_val = actual[key]
        exp_val = expected[key]

        assert isinstance(act_val, (int, float)), f"Value for '{key}' must be a float, got {type(act_val).__name__}."

        rel_error = abs(act_val - exp_val) / abs(exp_val) if exp_val != 0 else abs(act_val)
        assert rel_error <= 0.01, (
            f"Value for '{key}' is incorrect.\n"
            f"Actual: {act_val}\n"
            f"Expected: ~{exp_val}\n"
            f"Relative Error: {rel_error:.4f} (Must be <= 0.01)"
        )