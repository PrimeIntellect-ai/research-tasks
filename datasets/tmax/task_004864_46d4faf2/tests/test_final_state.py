# test_final_state.py

import os
import json
import sys
import subprocess
import pytest

def run_python_script(script):
    """Helper to run a Python script in a subprocess to use environment libraries like pandas/sklearn."""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True
    )
    return result

def test_files_exist():
    """Verify that the required output files were created."""
    assert os.path.isfile('/home/user/clean_data.parquet'), "/home/user/clean_data.parquet does not exist."
    assert os.path.isfile('/home/user/experiment.json'), "/home/user/experiment.json does not exist."

def test_experiment_json_format_and_values():
    """Verify the contents of experiment.json against expected computed values."""
    # Compute expected values using a subprocess to access pandas and sklearn
    compute_script = """
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
import json

df = pd.read_csv('/home/user/data.csv')
df['Ratio'] = df['Feature_A'] / df['Feature_B']
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

X = df[['Feature_A', 'Feature_B', 'Ratio']]
y = df['Target']

model = Ridge()
grid = GridSearchCV(model, param_grid={'alpha': [0.1, 1.0, 10.0]}, cv=5, scoring='neg_mean_squared_error')
grid.fit(X, y)

best_alpha = grid.best_params_['alpha']
best_mse = round(-grid.best_score_, 4)

print(json.dumps({'best_alpha': best_alpha, 'best_cv_mse': best_mse}))
"""
    result = run_python_script(compute_script)
    assert result.returncode == 0, f"Failed to compute expected values: {result.stderr}"

    expected_data = json.loads(result.stdout.strip())

    with open('/home/user/experiment.json', 'r') as f:
        try:
            student_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/experiment.json is not a valid JSON file.")

    assert "best_alpha" in student_data, "Missing 'best_alpha' key in experiment.json"
    assert "best_cv_mse" in student_data, "Missing 'best_cv_mse' key in experiment.json"

    assert abs(student_data["best_alpha"] - expected_data["best_alpha"]) < 1e-5, \
        f"Expected best_alpha {expected_data['best_alpha']}, got {student_data['best_alpha']}"

    assert abs(student_data["best_cv_mse"] - expected_data["best_cv_mse"]) < 1e-3, \
        f"Expected best_cv_mse {expected_data['best_cv_mse']}, got {student_data['best_cv_mse']}"

def test_parquet_schema_and_data():
    """Verify that the Parquet file has the correct schema and row count."""
    check_script = """
import pandas as pd
import numpy as np
import sys

try:
    df_original = pd.read_csv('/home/user/data.csv')
    df_original['Ratio'] = df_original['Feature_A'] / df_original['Feature_B']
    df_original.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_original.dropna(inplace=True)
    expected_len = len(df_original)

    pq_df = pd.read_parquet('/home/user/clean_data.parquet')

    if len(pq_df) != expected_len:
        print(f"Row count mismatch: expected {expected_len}, got {len(pq_df)}")
        sys.exit(1)

    if not pd.api.types.is_integer_dtype(pq_df['ID']):
        print(f"ID column is not an integer type. Got {pq_df['ID'].dtype}")
        sys.exit(2)

    for col in ['Feature_A', 'Feature_B', 'Ratio', 'Target']:
        if not pd.api.types.is_float_dtype(pq_df[col]):
            print(f"{col} column is not a float type. Got {pq_df[col].dtype}")
            sys.exit(3)

    sys.exit(0)
except Exception as e:
    print(str(e))
    sys.exit(4)
"""
    result = run_python_script(check_script)
    assert result.returncode == 0, f"Parquet validation failed: {result.stdout.strip() or result.stderr.strip()}"