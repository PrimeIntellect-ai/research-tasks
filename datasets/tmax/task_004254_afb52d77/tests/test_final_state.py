# test_final_state.py

import os
import sys
import json
import subprocess
import pytest

def test_output_file_exists():
    """Check if the final parquet file was created."""
    file_path = '/home/user/output/tracked_changes.parquet'
    assert os.path.isfile(file_path), f"The output file {file_path} does not exist."
    assert os.path.getsize(file_path) > 0, f"The output file {file_path} is empty."

def test_parquet_data_correctness():
    """
    Validate the contents of the parquet file using pandas via a subprocess.
    This avoids importing third-party libraries directly in the test suite,
    relying on the pandas installation required by the task.
    """
    file_path = '/home/user/output/tracked_changes.parquet'

    # Python script to read the parquet file and extract validation metrics
    validation_script = f"""
import json
import sys

try:
    import pandas as pd
except ImportError:
    print(json.dumps({{"error": "pandas is not installed"}}))
    sys.exit(0)

try:
    df = pd.read_parquet('{file_path}')

    # Ensure timestamp is a column
    if 'timestamp' not in df.columns:
        df = df.reset_index()

    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)

    servers = list(df['server'].unique())

    # Calculate sums
    srv01_counts = int(df[df['server'] == 'srv_01']['change_count'].sum())
    srv02_counts = int(df[df['server'] == 'srv_02']['change_count'].sum())

    # Get rolling values for srv_01 sorted by time
    srv01_df = df[df['server'] == 'srv_01'].sort_values('timestamp')
    srv01_rolling = srv01_df['rolling_3h_changes'].tolist()

    result = {{
        "servers": servers,
        "srv01_counts": srv01_counts,
        "srv02_counts": srv02_counts,
        "srv01_rolling": srv01_rolling
    }}
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
"""

    proc = subprocess.run(
        [sys.executable, "-c", validation_script],
        capture_output=True,
        text=True
    )

    assert proc.returncode == 0, f"Subprocess failed to execute: {proc.stderr}"

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse validation script output. Output was: {proc.stdout}")

    if "error" in data:
        pytest.fail(f"Error during data validation: {data['error']}")

    # Check normalization
    assert set(data['servers']) == {'srv_01', 'srv_02'}, (
        f"Server names were not normalized correctly. Found: {data['servers']}"
    )

    # Check total counts
    assert data['srv01_counts'] == 6, (
        f"Expected 6 total changes for srv_01, got {data['srv01_counts']}"
    )
    assert data['srv02_counts'] == 2, (
        f"Expected 2 total changes for srv_02, got {data['srv02_counts']}"
    )

    # Check rolling values
    expected_rolling = [2.0, 3.0, 3.0, 4.0]
    assert data['srv01_rolling'] == expected_rolling, (
        f"Rolling 3h changes for srv_01 are incorrect. Expected {expected_rolling}, got {data['srv01_rolling']}"
    )