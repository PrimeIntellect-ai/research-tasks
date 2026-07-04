# test_final_state.py

import os
import json
import subprocess
import pytest

RESULTS_PATH = "/home/user/pipeline/results.json"

def test_results_json_exists():
    """Check if the results.json file was generated."""
    assert os.path.isfile(RESULTS_PATH), f"Verification Failed: {RESULTS_PATH} not found."

def test_results_json_valid_and_keys():
    """Check if results.json is valid JSON and contains the correct keys."""
    try:
        with open(RESULTS_PATH, 'r') as f:
            results = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Verification Failed: {RESULTS_PATH} is not valid JSON.")
    except FileNotFoundError:
        pytest.fail(f"Verification Failed: {RESULTS_PATH} not found.")

    assert "oob_r2" in results, "Verification Failed: Missing 'oob_r2' key in results.json."
    assert "avg_inference_ms" in results, "Verification Failed: Missing 'avg_inference_ms' key in results.json."

    avg_inference = results["avg_inference_ms"]
    assert isinstance(avg_inference, float), "Verification Failed: avg_inference_ms must be a float."
    assert avg_inference > 0, "Verification Failed: avg_inference_ms must be a positive float."

def test_oob_r2_value():
    """Check if the computed oob_r2 matches the expected deterministic value."""
    # We compute the expected value dynamically using a subprocess to use pandas/sklearn
    # while keeping the test file itself free of third-party imports.
    script = """
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_csv('/home/user/pipeline/data.csv')
df = df.dropna()
df[['f1', 'f2', 'f3', 'f4']] = df[['f1', 'f2', 'f3', 'f4']].astype('float64')

np.random.seed(42)
train_df = df.sample(frac=1.0, replace=True, random_state=42)
oob_df = df.drop(train_df.index)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])

X_train = train_df[['f1', 'f2', 'f3', 'f4']]
y_train = train_df['target']
pipeline.fit(X_train, y_train)

X_test = oob_df[['f1', 'f2', 'f3', 'f4']]
y_test = oob_df['target']
expected_r2 = r2_score(y_test, pipeline.predict(X_test))
print(expected_r2)
"""
    result = subprocess.run(["python3", "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to compute expected R2: {result.stderr}"

    try:
        expected_r2 = float(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Failed to parse expected R2 from subprocess: {result.stdout}")

    try:
        with open(RESULTS_PATH, 'r') as f:
            results = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not read results.json: {e}")

    agent_r2 = results.get("oob_r2")
    assert agent_r2 is not None, "oob_r2 is missing from results.json."
    assert isinstance(agent_r2, float), "oob_r2 must be a float."

    assert abs(agent_r2 - expected_r2) <= 1e-4, f"Verification Failed: Expected oob_r2 near {expected_r2}, got {agent_r2}"