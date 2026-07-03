# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/events.db'
SCRIPT_PATH = '/home/user/etl_process.py'
OUTPUT_PATH = '/home/user/output.json'

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script file missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_index_exists():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_user_date';")
    index = cursor.fetchone()
    conn.close()
    assert index is not None, "Index 'idx_user_date' does not exist in the database."

def test_output_json_exists_and_format():
    assert os.path.exists(OUTPUT_PATH), f"Output file missing at {OUTPUT_PATH}"
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} is not a file"

    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} does not contain valid JSON")

    assert isinstance(data, list), "Output JSON must be a list of dictionaries"

    expected_data = [
        {"record_date": "2023-10-01", "rolling_sum": 1.0},
        {"record_date": "2023-10-02", "rolling_sum": 3.0},
        {"record_date": "2023-10-03", "rolling_sum": 6.0},
        {"record_date": "2023-10-04", "rolling_sum": 10.0},
        {"record_date": "2023-10-05", "rolling_sum": 15.0},
        {"record_date": "2023-10-06", "rolling_sum": 21.0},
        {"record_date": "2023-10-07", "rolling_sum": 28.0},
        {"record_date": "2023-10-08", "rolling_sum": 35.0},
        {"record_date": "2023-10-09", "rolling_sum": 42.0},
        {"record_date": "2023-10-10", "rolling_sum": 49.0}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Record at index {i} is not a dictionary"
        assert "record_date" in actual, f"Record at index {i} missing 'record_date'"
        assert "rolling_sum" in actual, f"Record at index {i} missing 'rolling_sum'"

        assert actual["record_date"] == expected["record_date"], \
            f"Record {i}: Expected date {expected['record_date']}, got {actual['record_date']}"

        # compare floats with small tolerance
        assert abs(float(actual["rolling_sum"]) - expected["rolling_sum"]) < 1e-5, \
            f"Record {i}: Expected rolling_sum {expected['rolling_sum']}, got {actual['rolling_sum']}"