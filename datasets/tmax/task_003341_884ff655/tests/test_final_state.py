# test_final_state.py
import os
import sys
import subprocess
import pytest

def test_parquet_file_exists():
    """Check that the output Parquet file exists at the correct absolute path."""
    expected_path = "/home/user/output/verified_reviews.parquet"
    assert os.path.isfile(expected_path), f"Output file {expected_path} is missing."

def test_parquet_contents_and_logic():
    """
    Validate the contents of the Parquet file using a subprocess.
    This ensures we only use the standard library in the pytest suite,
    while leveraging the pandas/pyarrow packages the student installed.
    """
    script = """
import sys
try:
    import pandas as pd
except ImportError:
    sys.stderr.write("pandas is not installed in the environment.\\n")
    sys.exit(1)

file_path = '/home/user/output/verified_reviews.parquet'
try:
    df = pd.read_parquet(file_path)
except Exception as e:
    sys.stderr.write(f"Failed to read parquet file: {e}\\n")
    sys.exit(1)

# Check row count (handling embedded newlines correctly)
if len(df) != 4:
    sys.stderr.write(f"Expected exactly 4 rows, got {len(df)}.\\n")
    sys.exit(1)

# Check required columns
required_columns = {'review_id', 'user_id', 'submitted_at', 'review_text', 'ingest_epoch', 'server_ip', 'is_verified'}
missing = required_columns - set(df.columns)
if missing:
    sys.stderr.write(f"Missing required columns: {missing}\\n")
    sys.exit(1)

# Verify data logic
df = df.set_index('review_id')

expected_verification = {
    'R001': True,
    'R002': False,
    'R003': True,
    'R004': True
}

for rid, expected_val in expected_verification.items():
    actual_val = bool(df.loc[rid, 'is_verified'])
    if actual_val != expected_val:
        sys.stderr.write(f"Review {rid} 'is_verified' should be {expected_val}, got {actual_val}.\\n")
        sys.exit(1)

# Check if embedded newlines were preserved correctly
if "Will never buy again.\\nEver." not in df.loc['R002', 'review_text']:
    sys.stderr.write("Embedded newlines were not parsed correctly for R002.\\n")
    sys.exit(1)

sys.exit(0)
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Parquet validation failed:\n{result.stderr.strip()}"