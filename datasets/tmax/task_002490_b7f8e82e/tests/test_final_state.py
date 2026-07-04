# test_final_state.py

import os
import subprocess
import pytest

def test_fixed_columns_file():
    """Verify that fixed_columns.txt exists and contains the correct sorted column names."""
    file_path = '/home/user/fixed_columns.txt'
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_columns = ['group_id', 'session_id', 'user_id']
    assert lines == expected_columns, f"Expected {expected_columns}, but got {lines} in {file_path}"

def test_processed_parquet_exists_and_schema():
    """Verify that processed.parquet exists and has the correct Int64 schema for _id columns."""
    file_path = '/home/user/processed.parquet'
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    # We use a subprocess to check the schema with pandas to strictly avoid third-party imports in the test file
    check_script = f"""
import pandas as pd
import sys

try:
    df = pd.read_parquet('{file_path}')
    errors = []
    for col in ['user_id', 'group_id', 'session_id']:
        if col not in df.columns:
            errors.append(f"Missing column: {{col}}")
        elif str(df[col].dtype) != 'Int64':
            errors.append(f"Column {{col}} has dtype {{df[col].dtype}}, expected Int64")

    if errors:
        print("; ".join(errors))
        sys.exit(1)
    sys.exit(0)
except Exception as e:
    print(f"Error reading parquet file: {{e}}")
    sys.exit(1)
"""

    result = subprocess.run(['python3', '-c', check_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Parquet schema verification failed: {result.stdout.strip()}"