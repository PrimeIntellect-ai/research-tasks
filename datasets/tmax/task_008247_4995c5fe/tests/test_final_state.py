# test_final_state.py

import os
import json
import csv
import math

def test_etl_log_validation_gate():
    log_path = "/home/user/etl.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_msg = "VALIDATION_GATE: Dropped 2 invalid records."
    assert expected_msg in log_content, (
        f"Could not find the exact validation gate message in {log_path}. "
        f"Expected to find: '{expected_msg}'"
    )

def test_clean_data_csv():
    csv_path = "/home/user/clean_data.csv"
    assert os.path.isfile(csv_path), f"Cleaned data file {csv_path} does not exist."

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert reader.fieldnames == ["timestamp", "sensor_id", "value"], (
        f"CSV headers are incorrect. Expected ['timestamp', 'sensor_id', 'value'], "
        f"got {reader.fieldnames}"
    )

    expected_data = [
        {"timestamp": 1696154400, "sensor_id": "A", "value": 10.0},
        {"timestamp": 1696154401, "sensor_id": "A", "value": 12.0},
        {"timestamp": 1696154402, "sensor_id": "A", "value": 25.0},
        {"timestamp": 1696154404, "sensor_id": "B", "value": 50.0},
        {"timestamp": 1696154405, "sensor_id": "B", "value": 30.0},
    ]

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows in {csv_path}, found {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_data)):
        assert int(actual["timestamp"]) == expected["timestamp"], f"Row {i+1}: timestamp mismatch"
        assert actual["sensor_id"] == expected["sensor_id"], f"Row {i+1}: sensor_id mismatch"
        assert math.isclose(float(actual["value"]), expected["value"], rel_tol=1e-5), f"Row {i+1}: value mismatch"

def test_anomalies_json():
    json_path = "/home/user/anomalies.json"
    assert os.path.isfile(json_path), f"Anomalies file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            anomalies = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert isinstance(anomalies, list), f"Expected anomalies to be a JSON array, got {type(anomalies).__name__}."

    expected_anomalies = [
        {
            "timestamp": 1696154402,
            "sensor_id": "A",
            "previous_value": 12.0,
            "current_value": 25.0,
            "difference": 13.0
        },
        {
            "timestamp": 1696154405,
            "sensor_id": "B",
            "previous_value": 50.0,
            "current_value": 30.0,
            "difference": 20.0
        }
    ]

    assert len(anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, found {len(anomalies)}."

    for i, (actual, expected) in enumerate(zip(anomalies, expected_anomalies)):
        assert actual.get("timestamp") == expected["timestamp"], f"Anomaly {i+1}: timestamp mismatch"
        assert actual.get("sensor_id") == expected["sensor_id"], f"Anomaly {i+1}: sensor_id mismatch"
        assert math.isclose(float(actual.get("previous_value", 0)), expected["previous_value"], rel_tol=1e-5), f"Anomaly {i+1}: previous_value mismatch"
        assert math.isclose(float(actual.get("current_value", 0)), expected["current_value"], rel_tol=1e-5), f"Anomaly {i+1}: current_value mismatch"
        assert math.isclose(float(actual.get("difference", 0)), expected["difference"], rel_tol=1e-5), f"Anomaly {i+1}: difference mismatch"