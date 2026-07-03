# test_final_state.py
import os
import json
import csv
import pytest

def get_expected_data():
    raw_csv_path = "/home/user/raw_sensors.csv"
    calib_json_path = "/home/user/calibrations.json"

    if not os.path.exists(raw_csv_path) or not os.path.exists(calib_json_path):
        # Fallback to default if inputs are missing/moved
        return [
            ["timestamp", "sensor_id", "corrected_value"],
            ["1620000000", "S1", "12.1000"],
            ["1620000001", "S2", "21.7580"],
            ["1620000002", "S1", "12.2200"],
            ["1620000004", "S2", "21.6600"]
        ], 4

    with open(calib_json_path, "r") as f:
        calibs = json.load(f)

    expected_rows = [["timestamp", "sensor_id", "corrected_value"]]
    valid_count = 0

    with open(raw_csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor_id = row["sensor_id"]
            if sensor_id in calibs:
                raw_val = float(row["raw_value"])
                scale = float(calibs[sensor_id]["scale"])
                offset = float(calibs[sensor_id]["offset"])
                corrected = (raw_val * scale) + offset
                expected_rows.append([row["timestamp"], sensor_id, f"{corrected:.4f}"])
                valid_count += 1

    return expected_rows, valid_count

def test_processed_csv_content():
    processed_path = "/home/user/processed.csv"
    assert os.path.isfile(processed_path), f"Missing output file: {processed_path}"

    expected_rows, _ = get_expected_data()

    with open(processed_path, "r") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in {processed_path}, got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}"

def test_metrics_txt_content():
    metrics_path = "/home/user/metrics.txt"
    assert os.path.isfile(metrics_path), f"Missing output file: {metrics_path}"

    _, expected_count = get_expected_data()
    expected_text = f"Total valid records: {expected_count}"

    with open(metrics_path, "r") as f:
        content = f.read().strip()

    assert content == expected_text, f"Content of {metrics_path} does not match expected. Expected '{expected_text}', got '{content}'"