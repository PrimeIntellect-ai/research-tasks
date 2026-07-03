# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/telemetry.db"
JSON_PATH = "/home/user/clean_backup.json"

def test_database_indices():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that old index is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_telemetry_node';")
    assert cursor.fetchone() is None, "The corrupted index 'idx_telemetry_node' was not dropped."

    # Check that new index exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_telemetry_optimal';")
    assert cursor.fetchone() is not None, "The new index 'idx_telemetry_optimal' was not created."

    # Check the columns of the new index
    cursor.execute("PRAGMA index_info('idx_telemetry_optimal');")
    columns = [row[2] for row in cursor.fetchall()]
    expected_columns = ['node_id', 'ts', 'metric']
    assert columns == expected_columns, f"Expected index columns {expected_columns}, but got {columns}."

    conn.close()

def test_json_export():
    assert os.path.isfile(JSON_PATH), f"Exported JSON file {JSON_PATH} is missing."

    with open(JSON_PATH, 'r') as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"The file {JSON_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "The exported JSON must be an array."

    # Check indentation (simple heuristic: check if it matches json.dumps with indent=2)
    # We will just verify the content first.
    expected_data = [
        {
            "telemetry_id": 101,
            "node_id": 1,
            "timestamp": "2023-10-01T10:00:00Z",
            "metric_value": 99.5
        },
        {
            "telemetry_id": 102,
            "node_id": 1,
            "timestamp": "2023-10-01T10:05:00Z",
            "metric_value": 98.2
        },
        {
            "telemetry_id": 105,
            "node_id": 4,
            "timestamp": "2023-10-01T10:15:00Z",
            "metric_value": 91.1
        }
    ]

    # Sort both lists by telemetry_id to ensure order doesn't cause failure
    data_sorted = sorted(data, key=lambda x: x.get('telemetry_id', 0))
    expected_sorted = sorted(expected_data, key=lambda x: x['telemetry_id'])

    assert len(data_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} records, found {len(data_sorted)}."

    for i, record in enumerate(data_sorted):
        expected = expected_sorted[i]
        assert isinstance(record.get('telemetry_id'), int), "telemetry_id must be an integer."
        assert isinstance(record.get('node_id'), int), "node_id must be an integer."
        assert isinstance(record.get('timestamp'), str), "timestamp must be a string."
        assert isinstance(record.get('metric_value'), float), "metric_value must be a float."

        assert record == expected, f"Record mismatch. Expected {expected}, got {record}."

    # Check indentation
    assert "\n  {" in content or "\n  \"" in content, "The JSON output must be formatted with an indent of 2 spaces."