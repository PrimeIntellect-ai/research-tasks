# test_final_state.py

import os
import json
import csv
import pytest

def read_csv(filepath):
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_cleaned_dataset_exists():
    assert os.path.isfile("/home/user/cleaned_dataset.csv"), "/home/user/cleaned_dataset.csv does not exist."

def test_summary_json_exists():
    assert os.path.isfile("/home/user/summary.json"), "/home/user/summary.json does not exist."

def test_cleaned_dataset_validity():
    cleaned_data = read_csv("/home/user/cleaned_dataset.csv")

    for i, row in enumerate(cleaned_data):
        target_str = row.get('target', '')
        assert target_str.strip() != '', f"Row {i} in cleaned_dataset.csv has a missing target."
        assert target_str.lower() != 'nan', f"Row {i} in cleaned_dataset.csv has a NaN target."

        try:
            target_val = float(target_str)
        except ValueError:
            pytest.fail(f"Row {i} in cleaned_dataset.csv has non-numeric target: {target_str}")

        assert target_val >= 0, f"Row {i} in cleaned_dataset.csv has a negative target: {target_val}"

def test_summary_json_keys_and_values():
    with open("/home/user/summary.json", "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not a valid JSON file.")

    expected_keys = {"best_alpha", "imputed_nan_count", "replaced_anomaly_count", "final_target_mean"}
    assert set(summary.keys()) == expected_keys, f"summary.json keys do not match. Expected {expected_keys}, got {set(summary.keys())}"

    assert summary["best_alpha"] in [0.1, 1.0, 10.0], f"best_alpha must be one of [0.1, 1.0, 10.0], got {summary['best_alpha']}"

    # Check original dataset for NaN count
    orig_data = read_csv("/home/user/dataset.csv")
    orig_nans = sum(1 for row in orig_data if row.get('target', '').strip() == '' or row.get('target', '').lower() == 'nan')
    assert summary["imputed_nan_count"] == orig_nans, f"imputed_nan_count should be {orig_nans}, got {summary['imputed_nan_count']}"

    # Check final_target_mean
    cleaned_data = read_csv("/home/user/cleaned_dataset.csv")
    targets = [float(row['target']) for row in cleaned_data]
    actual_mean = sum(targets) / len(targets)
    expected_mean_rounded = round(actual_mean, 4)

    assert round(summary["final_target_mean"], 4) == expected_mean_rounded, \
        f"final_target_mean should be {expected_mean_rounded}, got {summary['final_target_mean']}"

    # Check replaced_anomaly_count is an integer > 0 (since we know there are anomalies)
    assert isinstance(summary["replaced_anomaly_count"], int), "replaced_anomaly_count must be an integer."
    assert summary["replaced_anomaly_count"] > 0, "replaced_anomaly_count should be greater than 0."

def test_model_py_updated():
    with open("/home/user/model.py", "r") as f:
        content = f.read()

    # The original had self.fc1 = nn.Linear(3, 1)
    # Based on weights, it should be updated.
    assert "nn.Linear(3, 16)" in content or "nn.Linear(in_features=3, out_features=16)" in content, \
        "model.py does not seem to have the correct updated dimensions for fc1 (3 -> 16)."
    assert "nn.Linear(16, 8)" in content or "nn.Linear(in_features=16, out_features=8)" in content, \
        "model.py does not seem to have the correct updated dimensions for fc2 (16 -> 8)."
    assert "nn.Linear(8, 1)" in content or "nn.Linear(in_features=8, out_features=1)" in content, \
        "model.py does not seem to have the correct updated dimensions for fc3 (8 -> 1)."