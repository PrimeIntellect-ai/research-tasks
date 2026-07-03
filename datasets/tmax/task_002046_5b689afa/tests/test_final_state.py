# test_final_state.py

import os
import json
import subprocess
import pytest

def test_experiment_results_exist_and_successful():
    results_path = "/home/user/experiment_results.json"
    assert os.path.exists(results_path), f"File {results_path} does not exist. Did you run the benchmark script?"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    assert "status" in results, f"'status' key missing in {results_path}"
    assert results["status"] == "success", f"Expected status 'success', but got '{results['status']}'"

def test_parquet_schema_correct():
    parquet_path = "/home/user/processed_data.parquet"
    assert os.path.exists(parquet_path), f"File {parquet_path} does not exist. Did you run the ETL pipeline script?"

    # We use a subprocess to check the pandas dataframe type to strictly adhere to stdlib-only imports in the test file.
    checker_script = f"""
import sys
try:
    import pandas as pd
except ImportError:
    sys.exit(2)

try:
    df = pd.read_parquet('{parquet_path}')
    dtype_name = df['click_count'].dtype.name
    if dtype_name != 'Int64':
        print(f"Expected Int64, got {{dtype_name}}")
        sys.exit(1)
except Exception as e:
    print(str(e))
    sys.exit(3)
"""

    result = subprocess.run(
        ["python3", "-c", checker_script],
        capture_output=True,
        text=True
    )

    if result.returncode == 1:
        pytest.fail(f"Schema enforcement failed: {result.stdout.strip()}")
    elif result.returncode == 2:
        pytest.fail("Pandas is not installed in the environment.")
    elif result.returncode == 3:
        pytest.fail(f"Failed to read parquet file or check schema: {result.stdout.strip()}")

    assert result.returncode == 0, "Unknown error occurred while verifying the parquet schema."