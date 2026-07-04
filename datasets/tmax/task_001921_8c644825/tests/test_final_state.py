# test_final_state.py
import os
import pytest
import subprocess
import json
import hashlib

def get_parquet_data(filepath):
    """Helper to read parquet data using pandas via subprocess, returning a list of dicts."""
    script = f"""
import pandas as pd
import json
try:
    df = pd.read_parquet('{filepath}')
    # Convert to JSON for easy parsing in the test
    print(df.to_json(orient='records'))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
"""
    result = subprocess.run(['python3', '-c', script], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to execute pandas script for {filepath}:\n{result.stderr}"

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to decode JSON from pandas script. Output was: {result.stdout}")

    if isinstance(data, dict) and "error" in data:
        pytest.fail(f"Error reading parquet file {filepath}: {data['error']}")

    return data

def test_clean_data_files_exist():
    """Test that all 4 expected parquet files exist in the clean_data directory."""
    expected_files = [
        "hospital_1.parquet",
        "hospital_2.parquet",
        "hospital_3.parquet",
        "hospital_4.parquet"
    ]
    for f in expected_files:
        path = os.path.join("/home/user/clean_data", f)
        assert os.path.isfile(path), f"Expected output file {path} is missing."

def test_parquet_columns_and_anonymization():
    """Test that the parquet files have the correct columns and SSNs are properly hashed."""
    h1_path = "/home/user/clean_data/hospital_1.parquet"
    if not os.path.isfile(h1_path):
        pytest.skip(f"File {h1_path} not found.")

    data = get_parquet_data(h1_path)
    assert len(data) > 0, f"{h1_path} is empty."

    # Check columns
    expected_cols = {'patient_id', 'heart_rate', 'utc_timestamp'}
    actual_cols = set(data[0].keys())
    assert actual_cols == expected_cols, f"Incorrect columns in {h1_path}. Expected {expected_cols}, got {actual_cols}"

    # Check hashing for Bob Jones (SSN: 222-33-4444)
    expected_hash = hashlib.sha256('222-33-4444'.encode()).hexdigest()
    patient_ids = {row['patient_id'] for row in data}
    assert expected_hash in patient_ids, "SSN hashing failed or Bob Jones's records are missing."

def test_row_counts_and_nan_dropping():
    """Test that rows with missing heart rates are dropped and the total counts are correct."""
    # hospital_1: Alice has 4, Bob has 3 (1 missing) -> 7 total
    # hospital_2: Charlie has 3 (1 missing), Diana has 4 -> 7 total
    # hospital_3: Eve has 4 -> 4 total
    # hospital_4: Frank has 4 -> 4 total
    expected_counts = {
        "hospital_1.parquet": 7,
        "hospital_2.parquet": 7,
        "hospital_3.parquet": 4,
        "hospital_4.parquet": 4
    }

    for filename, expected_count in expected_counts.items():
        path = os.path.join("/home/user/clean_data", filename)
        if not os.path.isfile(path):
            continue

        data = get_parquet_data(path)
        assert len(data) == expected_count, f"Expected {expected_count} rows in {filename}, got {len(data)}"

def test_utc_timestamp_alignment():
    """Test that timestamps are correctly converted to UTC and formatted as ISO8601 strings ending in Z."""
    h1_path = "/home/user/clean_data/hospital_1.parquet"
    if not os.path.isfile(h1_path):
        pytest.skip(f"File {h1_path} not found.")

    data = get_parquet_data(h1_path)

    # Alice at 12:00 EDT on 2023-10-15 (America/New_York is UTC-4) -> 2023-10-15 16:00:00 UTC
    expected_utc = '2023-10-15T16:00:00Z'
    timestamps = [row['utc_timestamp'] for row in data]

    assert expected_utc in timestamps, f"Expected UTC timestamp {expected_utc} not found. Timezone conversion failed."

    # Check that all timestamps end with 'Z'
    for ts in timestamps:
        assert ts.endswith('Z'), f"Timestamp {ts} does not end with 'Z'."

def test_logging_output():
    """Test that the pipeline logged the correct messages to /home/user/pipeline.log."""
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        log_content = f.read()

    expected_logs = [
        "Successfully processed hospital_1.csv - 7 records generated",
        "Successfully processed hospital_2.csv - 7 records generated",
        "Successfully processed hospital_3.csv - 4 records generated",
        "Successfully processed hospital_4.csv - 4 records generated"
    ]

    for expected in expected_logs:
        assert expected in log_content, f"Expected log entry '{expected}' not found in {log_path}."