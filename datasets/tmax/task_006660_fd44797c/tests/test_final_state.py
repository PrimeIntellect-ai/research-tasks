# test_final_state.py

import os
import json
import subprocess

def test_metrics_json_content():
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} is missing."

    with open(metrics_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_path} is not a valid JSON file."

    expected_keys = {"total_rows_after_join", "rows_dropped", "outliers_capped"}
    assert set(metrics.keys()) == expected_keys, f"Metrics JSON must contain exactly keys: {expected_keys}"

    assert metrics["total_rows_after_join"] == 9, f"Expected 9 total_rows_after_join, got {metrics['total_rows_after_join']}"
    assert metrics["rows_dropped"] == 2, f"Expected 2 rows_dropped, got {metrics['rows_dropped']}"
    assert metrics["outliers_capped"] == 2, f"Expected 2 outliers_capped, got {metrics['outliers_capped']}"

def test_clean_data_parquet_validity():
    parquet_path = '/home/user/clean_data.parquet'
    assert os.path.isfile(parquet_path), f"Output file {parquet_path} is missing."

    # Using subprocess to check parquet file with pandas to strictly adhere to stdlib imports in the test file
    validation_script = f"""
import sys
try:
    import pandas as pd
except ImportError:
    print("Pandas not found, cannot validate parquet.")
    sys.exit(1)

try:
    df = pd.read_parquet('{parquet_path}')
except Exception as e:
    print(f"Failed to read parquet: {{e}}")
    sys.exit(1)

if 'account_tier' not in df.columns:
    print("account_tier column missing.")
    sys.exit(1)

if not pd.api.types.is_integer_dtype(df['account_tier']):
    print(f"account_tier must be an integer type, got {{df['account_tier'].dtype}}")
    sys.exit(1)

if 'activity_index' not in df.columns:
    print("activity_index column missing.")
    sys.exit(1)

if df['activity_index'].max() > 50.0:
    print(f"activity_index was not capped properly. Max value: {{df['activity_index'].max()}}")
    sys.exit(1)

if len(df) != 7:
    print(f"Expected 7 rows in final dataset, got {{len(df)}}")
    sys.exit(1)

# Check specific computed values for correctness
expected_activity = {{1: 0.0, 2: 50.0, 3: 32.0, 4: 50.0, 5: 6.4, 6: 0.0, 7: 0.0}}
for uid, expected_val in expected_activity.items():
    actual_val = df.loc[df['user_id'] == uid, 'activity_index'].values[0]
    if abs(actual_val - expected_val) > 1e-5:
        print(f"Incorrect activity_index for user {{uid}}: expected {{expected_val}}, got {{actual_val}}")
        sys.exit(1)

print("OK")
"""

    result = subprocess.run(
        ["python3", "-c", validation_script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Parquet validation failed:\n{result.stdout}\n{result.stderr}"
    assert result.stdout.strip() == "OK", f"Parquet validation script did not complete successfully: {result.stdout}"