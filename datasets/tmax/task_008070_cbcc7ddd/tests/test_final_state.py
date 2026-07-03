# test_final_state.py

import os
import json
import pytest
import subprocess

def run_python(script: str) -> str:
    """Helper to run a Python script in a subprocess and return its stdout."""
    res = subprocess.run(["python3", "-c", script], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Script failed: {res.stderr}")
    return res.stdout.strip()

def test_phase1_parquet_exists_and_valid():
    """Verify that the cleaned dataset is saved as a Parquet file and respects schema constraints."""
    parquet_path = '/home/user/astro_data/clean_data.parquet'
    assert os.path.exists(parquet_path), f"Parquet file missing: {parquet_path}"

    script = f"""
import pandas as pd
try:
    df = pd.read_parquet('{parquet_path}')
    print(len(df))
    print((df['mass'] > 0).all())
    print((df['radius'].astype(float) > 0).all())
    print(df['status'].isin(['confirmed', 'false_positive']).all())
except Exception as e:
    print(f"ERROR: {{e}}")
"""
    output = run_python(script).splitlines()
    assert not output[0].startswith("ERROR"), f"Failed to read parquet file: {output[0]}"
    assert len(output) >= 4, "Unexpected output from validation script"

    assert output[0] == "4956", f"Expected 4956 valid rows after dropping invalid ones, got {output[0]}"
    assert output[1] == "True", "Found rows with mass <= 0"
    assert output[2] == "True", "Found rows with radius <= 0"
    assert output[3] == "True", "Found rows with invalid status"

def test_phase2_bootstrap_ci():
    """Verify the bootstrap confidence interval was computed correctly and saved properly."""
    ci_path = '/home/user/astro_data/bootstrap_ci.txt'
    assert os.path.exists(ci_path), f"Bootstrap CI file missing: {ci_path}"

    # Compute the expected CI using the same seed and method
    script = """
import pandas as pd
import numpy as np
df = pd.read_parquet('/home/user/astro_data/clean_data.parquet')
df_conf = df[df['status'] == 'confirmed']
radii_conf = df_conf['radius'].astype(float).values
np.random.seed(42)
means = [np.mean(np.random.choice(radii_conf, size=len(radii_conf), replace=True)) for _ in range(1000)]
print(f"{np.percentile(means, 2.5):.4f},{np.percentile(means, 97.5):.4f}")
"""
    expected_ci = run_python(script)
    exp_lower, exp_upper = map(float, expected_ci.split(','))

    with open(ci_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 2, f"Bootstrap CI file must contain exactly two comma-separated values, got: {content}"

    try:
        act_lower, act_upper = map(float, parts)
    except ValueError:
        pytest.fail(f"Could not parse floats from bootstrap_ci.txt: {content}")

    assert abs(act_lower - exp_lower) < 1e-3, f"Expected lower CI bound ~{exp_lower}, got {act_lower}"
    assert abs(act_upper - exp_upper) < 1e-3, f"Expected upper CI bound ~{exp_upper}, got {act_upper}"

def test_phase3_metrics():
    """Verify the model evaluation metrics are computed correctly and saved as JSON."""
    metrics_path = '/home/user/astro_data/metrics.json'
    assert os.path.exists(metrics_path), f"Metrics file missing: {metrics_path}"

    # Compute the expected metrics
    script = """
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

df = pd.read_parquet('/home/user/astro_data/clean_data.parquet')

# Regression
df_conf = df[df['status'] == 'confirmed']
X_reg = df_conf[['mass', 'orbital_period']].values
y_reg = df_conf['radius'].values
rf = RandomForestRegressor(random_state=42)
mse_scores = cross_val_score(rf, X_reg, y_reg, cv=5, scoring='neg_mean_squared_error')
rmse = np.sqrt(np.mean(-mse_scores))

# Classification
X_clf = df[['mass', 'radius', 'orbital_period']].values
y_clf = df['status'].values
lr = LogisticRegression(random_state=42)
f1_scores = cross_val_score(lr, X_clf, y_clf, cv=5, scoring='f1_macro')
f1 = np.mean(f1_scores)

print(f"{rmse:.4f},{f1:.4f}")
"""
    expected_metrics = run_python(script)
    exp_rmse, exp_f1 = map(float, expected_metrics.split(','))

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not valid JSON")

    assert "rmse" in metrics, "Missing 'rmse' key in metrics.json"
    assert "f1" in metrics, "Missing 'f1' key in metrics.json"

    assert isinstance(metrics["rmse"], (int, float)), "rmse must be a number"
    assert isinstance(metrics["f1"], (int, float)), "f1 must be a number"

    assert abs(metrics["rmse"] - exp_rmse) < 1e-3, f"Expected RMSE ~{exp_rmse}, got {metrics['rmse']}"
    assert abs(metrics["f1"] - exp_f1) < 1e-3, f"Expected F1 ~{exp_f1}, got {metrics['f1']}"