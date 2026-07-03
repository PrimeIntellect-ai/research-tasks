# test_final_state.py

import os
import subprocess
import pytest

def test_processed_data_exists():
    """Verify that the processed_data.parquet file was created."""
    output_path = '/home/user/processed_data.parquet'
    assert os.path.exists(output_path), f"Error: {output_path} does not exist."
    assert os.path.isfile(output_path), f"Error: {output_path} is not a file."

def test_processed_data_content():
    """Verify the content of the processed_data.parquet file using a subprocess."""
    output_path = '/home/user/processed_data.parquet'
    assert os.path.exists(output_path), "Output file missing, cannot verify content."

    # We use a subprocess to use the virtual environment's pandas/pyarrow
    # since we are restricted to standard library in the test script itself.
    python_executable = '/home/user/venv/bin/python'
    if not os.path.exists(python_executable):
        # Fallback to system python if venv is not used or missing
        python_executable = 'python3'

    script = f"""
import sys
try:
    import pandas as pd
except ImportError:
    print("pandas not installed")
    sys.exit(1)

try:
    df = pd.read_parquet('{output_path}')
except Exception as e:
    print(f"Failed to read parquet: {{e}}")
    sys.exit(1)

if len(df) != 96:
    print(f"Expected 96 rows, found {{len(df)}}")
    sys.exit(2)

expected_columns = {{'id', 'f1', 'f2', 'f3', 'predicted_label', 'probability'}}
if set(df.columns) != expected_columns:
    print(f"Columns do not match expected schema. Found {{list(df.columns)}}")
    sys.exit(3)

if not (df['probability'].between(0, 1)).all():
    print("Invalid probabilities found (not between 0 and 1).")
    sys.exit(4)

prob_mean = df['probability'].mean()
if not (0.3 < prob_mean < 0.7):
    print(f"Probability mean {{prob_mean}} is out of expected distribution.")
    sys.exit(5)

print("SUCCESS")
"""

    try:
        result = subprocess.run(
            [python_executable, '-c', script],
            capture_output=True,
            text=True,
            check=True
        )
        assert "SUCCESS" in result.stdout, "Verification script did not succeed."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Data verification failed with exit code {e.returncode}. Output: {e.stdout.strip()} {e.stderr.strip()}")