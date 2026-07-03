# test_final_state.py
import os
import csv
import json
import math
import pytest

CLEANED_DATA_PATH = "/home/user/cleaned_data.csv"
METRICS_PATH = "/home/user/experiment_metrics.json"

def test_cleaned_data_csv():
    assert os.path.exists(CLEANED_DATA_PATH), f"File {CLEANED_DATA_PATH} does not exist."
    assert os.path.isfile(CLEANED_DATA_PATH), f"Path {CLEANED_DATA_PATH} is not a file."

    expected_rows = [
        ["ID", "Timestamp", "Temperature", "Humidity", "Location", "Model"],
        ["1", "2023-10-01T00:00:00Z", "22.5", "45.0", "Lab1", "X100"],
        ["2", "2023-10-01T00:00:00Z", "23.0", "40.0", "Lab2", "Y200"],
        ["3", "2023-10-01T00:00:00Z", "21.0", "50.0", "Lab1", "X100"]
    ]

    with open(CLEANED_DATA_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in {CLEANED_DATA_PATH}, got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i} mismatch in {CLEANED_DATA_PATH}. Expected {expected}, got {actual}."

def test_experiment_metrics_json():
    assert os.path.exists(METRICS_PATH), f"File {METRICS_PATH} does not exist."
    assert os.path.isfile(METRICS_PATH), f"Path {METRICS_PATH} is not a file."

    with open(METRICS_PATH, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {METRICS_PATH} is not valid JSON.")

    expected_keys = {
        "initial_rows",
        "rows_after_missing_drop",
        "rows_after_outlier_drop",
        "final_mean_temperature"
    }

    assert set(metrics.keys()) == expected_keys, f"Metrics keys mismatch. Expected {expected_keys}, got {set(metrics.keys())}."

    assert metrics["initial_rows"] == 7, f"Expected initial_rows to be 7, got {metrics['initial_rows']}."
    assert metrics["rows_after_missing_drop"] == 5, f"Expected rows_after_missing_drop to be 5, got {metrics['rows_after_missing_drop']}."
    assert metrics["rows_after_outlier_drop"] == 3, f"Expected rows_after_outlier_drop to be 3, got {metrics['rows_after_outlier_drop']}."

    expected_mean = (22.5 + 23.0 + 21.0) / 3
    assert math.isclose(metrics["final_mean_temperature"], expected_mean, rel_tol=1e-5), f"Expected final_mean_temperature to be approx {expected_mean}, got {metrics['final_mean_temperature']}."