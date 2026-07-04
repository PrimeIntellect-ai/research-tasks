# test_final_state.py

import os
import json
import csv
import pytest

def test_cleaned_data_exists_and_correct():
    cleaned_file = "/home/user/cleaned_sensor_data.csv"
    assert os.path.isfile(cleaned_file), f"File {cleaned_file} is missing."

    expected_rows = [
        ["timestamp", "sensor_id", "temperature", "humidity", "status"],
        ["2023-01-01T00:00:00Z", "S1", "22.5", "45.0", "ACTIVE"],
        ["2023-01-01T00:01:00Z", "S2", "25.0", "50.0", "ACTIVE"],
        ["2023-01-01T00:05:00Z", "S1", "25.0", "99.9", "ACTIVE"],
        ["2023-01-01T00:06:00Z", "S3", "19.5", "40.0", "ACTIVE"],
        ["2023-01-01T00:07:00Z", "S1", "20.0", "0.0", "ACTIVE"],
        ["2023-01-01T00:08:00Z", "S2", "22.0", "100.0", "ACTIVE"]
    ]

    with open(cleaned_file, "r") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in cleaned data, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_json_metrics_generated_correctly():
    metrics_file = "/home/user/best_model_metrics.json"
    assert os.path.isfile(metrics_file), f"File {metrics_file} was not generated."

    with open(metrics_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_file} does not contain valid JSON.")

    assert "best_alpha" in data, "Key 'best_alpha' missing from metrics JSON."
    assert "rows_trained" in data, "Key 'rows_trained' missing from metrics JSON."

    assert data["rows_trained"] == 6, f"Expected 'rows_trained' to be 6, got {data['rows_trained']}."
    assert data["best_alpha"] == 0.1, f"Expected 'best_alpha' to be 0.1, got {data['best_alpha']}."

def test_script_exists():
    script_file = "/home/user/etl_pipeline.sh"
    assert os.path.isfile(script_file), f"Script {script_file} is missing."