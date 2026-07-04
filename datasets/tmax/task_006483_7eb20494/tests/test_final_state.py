# test_final_state.py

import os
import json
import sys
import subprocess
import pytest

def test_summary_json():
    """Test that summary.json exists and contains the correct aggregated data."""
    json_path = '/home/user/summary.json'
    assert os.path.exists(json_path), f"JSON summary file not found at {json_path}"

    with open(json_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected_summary = [
        {"server_id": "srv-01", "total_errors": 3, "top_word": "connection", "top_word_count": 3},
        {"server_id": "srv-02", "total_errors": 2, "top_word": "for", "top_word_count": 2},
        {"server_id": "srv-03", "total_errors": 1, "top_word": "crash", "top_word_count": 1}
    ]

    assert isinstance(summary, list), "JSON root should be a list."
    assert len(summary) == len(expected_summary), f"Expected {len(expected_summary)} servers in summary, got {len(summary)}."

    # Check exact match since order should be alphabetical by server_id
    assert summary == expected_summary, f"JSON summary content mismatch. Expected {expected_summary}, got {summary}"

def test_parquet_file():
    """Test that word_counts.parquet exists, is a valid parquet file, and contains correct data."""
    parquet_path = '/home/user/word_counts.parquet'
    assert os.path.exists(parquet_path), f"Parquet file not found at {parquet_path}"

    # Check Parquet magic bytes (PAR1)
    with open(parquet_path, 'rb') as f:
        magic = f.read(4)
        assert magic == b'PAR1', f"File {parquet_path} does not appear to be a valid Parquet file (missing PAR1 magic bytes)."

    # Use a subprocess to verify the content using pandas/pyarrow, 
    # as the student was required to install them and we must restrict to stdlib in the test suite itself.
    verify_script = f"""
import sys
try:
    import pandas as pd
except ImportError:
    print("pandas not installed")
    sys.exit(1)

try:
    df = pd.read_parquet('{parquet_path}')
except Exception as e:
    print(f"Failed to read parquet: {{e}}")
    sys.exit(1)

if len(df) != 19:
    print(f"Expected 19 rows, got {{len(df)}}")
    sys.exit(1)

# Check sorting and first row
row0 = df.iloc[0]
if row0['server_id'] != 'srv-01' or row0['word'] != 'connection' or row0['count'] != 3:
    print(f"First row mismatch. Got: {{row0.to_dict()}}")
    sys.exit(1)

# Check another specific row to ensure sorting (count descending, then word ascending)
# srv-01: connection(3), database(2), timeout(2), by(1), peer(1), reset(1)
# row 1 should be database (2)
row1 = df.iloc[1]
if row1['server_id'] != 'srv-01' or row1['word'] != 'database' or row1['count'] != 2:
    print(f"Second row mismatch. Got: {{row1.to_dict()}}")
    sys.exit(1)

print("SUCCESS")
"""

    result = subprocess.run([sys.executable, '-c', verify_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Parquet content verification failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert "SUCCESS" in result.stdout, "Parquet verification script did not output SUCCESS."