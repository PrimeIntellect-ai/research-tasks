# test_final_state.py
import os
import sys
import json
import hashlib
import subprocess
import pytest

PARQUET_PATH = '/home/user/unified_sensors.parquet'

def get_parquet_data():
    if not os.path.exists(PARQUET_PATH):
        pytest.fail(f"File not found: {PARQUET_PATH}")

    # We use a subprocess to read the parquet file using pandas, 
    # since third-party libraries cannot be directly imported in the test file.
    script = """
import sys
import json
try:
    import pandas as pd
    df = pd.read_parquet('/home/user/unified_sensors.parquet')

    # Ensure standard types for JSON serialization
    df['timestamp'] = df['timestamp'].astype(str)
    df['sensor_id'] = df['sensor_id'].astype(str)
    df['value'] = df['value'].astype(float)
    df['record_hash'] = df['record_hash'].astype(str)

    # Output as JSON
    print(df.to_json(orient='records'))
except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
"""
    result = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Failed to read parquet file. Ensure pandas and a parquet engine (pyarrow/fastparquet) are installed. Error: {result.stderr}")

    try:
        data = json.loads(result.stdout)
        return data
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse parquet data: {result.stdout}")

def test_parquet_file_exists():
    assert os.path.isfile(PARQUET_PATH), f"The finalized file {PARQUET_PATH} does not exist."

def test_parquet_schema_and_row_count():
    data = get_parquet_data()

    # We expect 6 rows from factory 1 and 4 rows from factory 2.
    # 2 rows in factory 2 are exact duplicates of factory 1 data.
    # Total unique rows = 8.
    assert len(data) == 8, f"Expected exactly 8 deduplicated rows, but got {len(data)}."

    expected_columns = {'timestamp', 'sensor_id', 'value', 'record_hash'}
    for idx, row in enumerate(data):
        assert set(row.keys()) == expected_columns, f"Row {idx} columns {set(row.keys())} do not match expected {expected_columns}."

def test_parquet_data_normalization_and_hash():
    data = get_parquet_data()

    for idx, row in enumerate(data):
        ts = row['timestamp']
        sensor = row['sensor_id']
        val = row['value']
        rec_hash = row['record_hash']

        # Check ISO 8601 strict format with Z
        assert ts.endswith('Z') and '+' not in ts, f"Row {idx}: Timestamp '{ts}' is not in strict ISO 8601 format ending with 'Z'."
        assert len(ts) == 20 and ts[10] == 'T', f"Row {idx}: Timestamp '{ts}' is not formatted as YYYY-MM-DDTHH:MM:SSZ."

        # Check lowercase sensor_id
        assert sensor.islower(), f"Row {idx}: Sensor ID '{sensor}' is not entirely lowercase."

        # Check value is float
        assert isinstance(val, float), f"Row {idx}: Value {val} is not a float."

        # Verify MD5 Hash logic
        expected_str = f"{ts}_{sensor}_{val:.2f}"
        expected_hash = hashlib.md5(expected_str.encode('utf-8')).hexdigest()

        assert rec_hash == expected_hash, f"Row {idx}: Hash mismatch for '{expected_str}'. Expected {expected_hash}, got {rec_hash}."

def test_parquet_sorting():
    data = get_parquet_data()

    for i in range(1, len(data)):
        prev = data[i-1]
        curr = data[i]

        if prev['timestamp'] == curr['timestamp']:
            assert prev['sensor_id'] <= curr['sensor_id'], f"Data is not sorted by sensor_id for identical timestamp {prev['timestamp']}."
        else:
            assert prev['timestamp'] < curr['timestamp'], "Data is not sorted by timestamp in ascending order."