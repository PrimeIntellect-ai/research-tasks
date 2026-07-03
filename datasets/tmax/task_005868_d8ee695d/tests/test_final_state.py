# test_final_state.py

import os
import csv
import json
import pytest

JOINED_DATA_PATH = "/home/user/output/joined_data.csv"
METRICS_PATH = "/home/user/output/metrics.json"

def test_joined_data_exists():
    """Verify that the joined_data.csv file was created."""
    assert os.path.isfile(JOINED_DATA_PATH), f"File {JOINED_DATA_PATH} does not exist."

def test_joined_data_content():
    """Verify the content and type handling in joined_data.csv."""
    assert os.path.isfile(JOINED_DATA_PATH), f"File {JOINED_DATA_PATH} does not exist."

    with open(JOINED_DATA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0, f"File {JOINED_DATA_PATH} is empty."

    # Check headers
    expected_headers = {"machine_id", "temp", "vibration", "days_since_last_service", "failed"}
    actual_headers = set(reader.fieldnames)
    assert expected_headers.issubset(actual_headers), f"Missing expected columns. Found: {actual_headers}"

    # Check machine 2 for missing maintenance filled with -1
    machine_2_row = next((row for row in rows if row["machine_id"] == "2"), None)
    assert machine_2_row is not None, "Row for machine_id=2 is missing."

    days_val = machine_2_row["days_since_last_service"]
    assert days_val == "-1", f"Expected '-1' for missing maintenance, got '{days_val}'."

    # Ensure no floats in days_since_last_service
    for row in rows:
        val = row["days_since_last_service"]
        assert "." not in val, f"Found float representation '{val}' in days_since_last_service, expected integer."

def test_metrics_json_exists():
    """Verify that the metrics.json file was created."""
    assert os.path.isfile(METRICS_PATH), f"File {METRICS_PATH} does not exist."

def test_metrics_json_content():
    """Verify the content of metrics.json."""
    assert os.path.isfile(METRICS_PATH), f"File {METRICS_PATH} does not exist."

    with open(METRICS_PATH, 'r', encoding='utf-8') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {METRICS_PATH} is not valid JSON.")

    assert "accuracy" in metrics, "Key 'accuracy' missing in metrics.json."
    assert "inference_micros_per_row" in metrics, "Key 'inference_micros_per_row' missing in metrics.json."

    accuracy = metrics["accuracy"]
    inference_time = metrics["inference_micros_per_row"]

    assert isinstance(accuracy, float), f"Expected 'accuracy' to be a float, got {type(accuracy).__name__}."
    assert isinstance(inference_time, float), f"Expected 'inference_micros_per_row' to be a float, got {type(inference_time).__name__}."

    assert 0.0 <= accuracy <= 1.0, f"Accuracy {accuracy} is out of bounds [0.0, 1.0]."
    assert inference_time > 0.0, f"Inference time {inference_time} should be strictly positive."