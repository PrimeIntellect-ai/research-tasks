# test_final_state.py
import os
import json
import pytest

def test_processed_directory_exists():
    assert os.path.isdir('/home/user/processed'), "The directory /home/user/processed was not created."

def test_clean_data_json():
    filepath = '/home/user/processed/clean_data.json'
    assert os.path.isfile(filepath), f"The file {filepath} was not created."

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {filepath} does not contain valid JSON.")

    assert isinstance(data, list), f"{filepath} must contain a JSON array."

    expected_data = [
        {"tx_id": "T001", "timestamp": "2023-10-01T10:00:00Z", "user_id": "U1", "amount": 100.0},
        {"tx_id": "T002", "timestamp": "2023-10-01T12:00:00Z", "user_id": "U2", "amount": 150.0},
        {"tx_id": "T003", "timestamp": "2023-10-02T10:00:00Z", "user_id": "U1", "amount": 120.0},
        {"tx_id": "T004", "timestamp": "2023-10-02T10:00:00Z", "user_id": "U3", "amount": 400.0},
        {"tx_id": "T005", "timestamp": "2023-10-03T11:00:00Z", "user_id": "U4", "amount": 260.0}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records in {filepath}, but found {len(data)}."

    for i, expected_record in enumerate(expected_data):
        actual_record = data[i]
        assert actual_record.get("tx_id") == expected_record["tx_id"], f"Record {i} tx_id mismatch."
        assert actual_record.get("timestamp") == expected_record["timestamp"], f"Record {i} timestamp mismatch."
        assert actual_record.get("user_id") == expected_record["user_id"], f"Record {i} user_id mismatch."
        assert float(actual_record.get("amount", 0)) == expected_record["amount"], f"Record {i} amount mismatch."

def test_anomalies_json():
    filepath = '/home/user/processed/anomalies.json'
    assert os.path.isfile(filepath), f"The file {filepath} was not created."

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {filepath} does not contain valid JSON.")

    assert isinstance(data, list), f"{filepath} must contain a JSON array."

    expected_anomalies = [
        {
            "date": "2023-10-02",
            "previous_avg": 125.0,
            "current_avg": 260.0,
            "deviation_pct": 108.0
        }
    ]

    assert len(data) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies in {filepath}, but found {len(data)}."

    for i, expected_record in enumerate(expected_anomalies):
        actual_record = data[i]
        assert actual_record.get("date") == expected_record["date"], f"Anomaly {i} date mismatch."
        assert float(actual_record.get("previous_avg", 0)) == expected_record["previous_avg"], f"Anomaly {i} previous_avg mismatch."
        assert float(actual_record.get("current_avg", 0)) == expected_record["current_avg"], f"Anomaly {i} current_avg mismatch."

        # Allow a small float precision tolerance for deviation_pct
        actual_deviation = float(actual_record.get("deviation_pct", 0))
        assert abs(actual_deviation - expected_record["deviation_pct"]) < 0.1, f"Anomaly {i} deviation_pct mismatch. Expected {expected_record['deviation_pct']}, got {actual_deviation}."

def test_go_program_exists():
    assert os.path.isfile('/home/user/etl_pipeline.go'), "The Go program /home/user/etl_pipeline.go is missing."