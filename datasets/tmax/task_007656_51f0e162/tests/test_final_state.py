# test_final_state.py

import os
import json
import csv
import pytest

def test_processed_data_csv():
    processed_data_path = "/home/user/processed_data.csv"
    assert os.path.isfile(processed_data_path), f"Processed data file {processed_data_path} is missing."

    with open(processed_data_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Processed data file is empty."

    header = rows[0]
    assert header == ["f_new", "f3"], f"Expected header ['f_new', 'f3'], but got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows, but got {len(data_rows)}"

    # Compute expected values from raw_data logic
    # f1 mean = (10 + 20 + 30) / 3 = 20
    # Row 1: f1=10, f2=50 -> f_new=500, f3=1
    # Row 2: f1=20(imputed), f2=60 -> f_new=1200, f3=2
    # Row 3 (was Row 4): f1=30, f2=40 -> f_new=1200, f3=4
    expected_data = [
        (500.0, 1.0),
        (1200.0, 2.0),
        (1200.0, 4.0)
    ]

    for i, (expected_f_new, expected_f3) in enumerate(expected_data):
        actual_f_new = float(data_rows[i][0])
        actual_f3 = float(data_rows[i][1])

        assert abs(actual_f_new - expected_f_new) < 1e-5, f"Row {i+1}: Expected f_new={expected_f_new}, got {actual_f_new}"
        assert abs(actual_f3 - expected_f3) < 1e-5, f"Row {i+1}: Expected f3={expected_f3}, got {actual_f3}"

def test_experiment_artifact_json():
    artifact_path = "/home/user/experiment_artifact.json"
    assert os.path.isfile(artifact_path), f"Experiment artifact file {artifact_path} is missing."

    with open(artifact_path, 'r') as f:
        try:
            artifact = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {artifact_path} is not valid JSON.")

    assert "rows" in artifact, "Key 'rows' is missing in experiment artifact."
    assert "f_new_mean" in artifact, "Key 'f_new_mean' is missing in experiment artifact."

    assert artifact["rows"] == 3, f"Expected 'rows' to be 3, got {artifact['rows']}"

    expected_mean = 966.67
    actual_mean = artifact["f_new_mean"]
    assert isinstance(actual_mean, (int, float)), f"'f_new_mean' should be a number, got {type(actual_mean)}"
    assert abs(actual_mean - expected_mean) < 1e-2, f"Expected 'f_new_mean' to be {expected_mean}, got {actual_mean}"