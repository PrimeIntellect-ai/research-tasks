# test_final_state.py

import os
import json
import hashlib
from datetime import datetime

def hash_uid(uid):
    return "anon_" + hashlib.sha256(uid.encode('utf-8')).hexdigest()

def test_processed_directory_exists():
    assert os.path.isdir('/home/user/processed'), "The /home/user/processed directory was not created."

def test_unified_parquet_exists_and_valid():
    file_path = '/home/user/processed/unified.parquet'
    assert os.path.isfile(file_path), f"{file_path} is missing."

    # Check Parquet magic bytes since third-party libs are not allowed in tests
    with open(file_path, 'rb') as f:
        header = f.read(4)
        f.seek(-4, os.SEEK_END)
        footer = f.read(4)
    assert header == b'PAR1', "unified.parquet does not have a valid Parquet header."
    assert footer == b'PAR1', "unified.parquet does not have a valid Parquet footer."

def test_alerts_json():
    file_path = '/home/user/processed/alerts.json'
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            alerts = json.load(f)
        except json.JSONDecodeError:
            assert False, "alerts.json is not a valid JSON file."

    assert isinstance(alerts, list), "alerts.json must contain a JSON array."
    assert len(alerts) == 3, f"Expected exactly 3 alerts, found {len(alerts)}."

    # Expected alerts based on raw data processing logic
    expected_alerts = [
        {
            "timestamp": "2023-10-01 10:05:00",
            "user_id": hash_uid("patient_1"),
            "value": 110.0,
            "alert_type": "changepoint"
        },
        {
            "timestamp": "2023-10-01 10:10:00",
            "user_id": hash_uid("patient_2"),
            "value": 38.0,
            "alert_type": "both"
        },
        {
            "timestamp": "2023-10-01 10:15:00",
            "user_id": hash_uid("patient_1"),
            "value": 160.0,
            "alert_type": "both"
        }
    ]

    for i, expected in enumerate(expected_alerts):
        actual = alerts[i]

        # Check keys
        for key in ["timestamp", "user_id", "value", "alert_type"]:
            assert key in actual, f"Alert at index {i} is missing the '{key}' key."

        # Parse and compare timestamp to handle slight formatting differences (e.g., 'T', 'Z')
        actual_ts_str = actual["timestamp"].replace("T", " ").replace("Z", "")
        expected_ts_str = expected["timestamp"]
        assert actual_ts_str == expected_ts_str, f"Alert {i} timestamp mismatch: expected {expected_ts_str}, got {actual['timestamp']}."

        assert actual["user_id"] == expected["user_id"], f"Alert {i} user_id mismatch: expected {expected['user_id']}, got {actual['user_id']}."
        assert float(actual["value"]) == expected["value"], f"Alert {i} value mismatch: expected {expected['value']}, got {actual['value']}."
        assert actual["alert_type"] == expected["alert_type"], f"Alert {i} alert_type mismatch: expected {expected['alert_type']}, got {actual['alert_type']}."