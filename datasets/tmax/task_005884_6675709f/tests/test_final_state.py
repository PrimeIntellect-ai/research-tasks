# test_final_state.py

import os
import json
import csv
import pytest

REPORT_PATH = "/home/user/report.json"
CLEANED_CSV_PATH = "/home/user/cleaned_sensors.csv"

def test_report_exists_and_valid():
    """Test that the report.json exists and contains the correct values."""
    assert os.path.isfile(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not a valid JSON file.")

    assert "dropped_column" in report, "Key 'dropped_column' missing in report."
    assert report["dropped_column"] == "sensor_B", f"Expected dropped_column to be 'sensor_B', got {report['dropped_column']}"

    assert "bootstrap_mean_sensor_D" in report, "Key 'bootstrap_mean_sensor_D' missing in report."
    mean_d = report["bootstrap_mean_sensor_D"]
    assert isinstance(mean_d, (int, float)), "bootstrap_mean_sensor_D must be a number."
    assert 99.0 <= mean_d <= 101.0, f"Bootstrap mean {mean_d} is out of expected bounds (99.0 - 101.0)."

    assert "best_ridge_alpha" in report, "Key 'best_ridge_alpha' missing in report."
    alpha = report["best_ridge_alpha"]
    assert alpha in [0.1, 1.0, 10.0], f"best_ridge_alpha {alpha} is not in the allowed grid [0.1, 1.0, 10.0]."

def test_cleaned_dataset_exists_and_valid():
    """Test that cleaned_sensors.csv exists, has sensor_B removed, and has no missing target_temp."""
    assert os.path.isfile(CLEANED_CSV_PATH), f"Cleaned dataset missing at {CLEANED_CSV_PATH}"

    with open(CLEANED_CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail("Cleaned dataset is empty.")

        assert "sensor_B" not in headers, "sensor_B was not removed from the final CSV."
        assert "target_temp" in headers, "target_temp column missing in the final CSV."

        target_idx = headers.index("target_temp")

        for row_num, row in enumerate(reader, start=2):
            if not row:
                continue
            assert len(row) > target_idx, f"Row {row_num} is malformed."
            val = row[target_idx].strip()
            assert val != "", f"Missing value found in target_temp at row {row_num}."
            assert val.lower() not in ["nan", "null", "na"], f"Unimputed missing value '{val}' found in target_temp at row {row_num}."