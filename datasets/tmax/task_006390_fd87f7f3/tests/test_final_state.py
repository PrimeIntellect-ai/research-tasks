# test_final_state.py
import os
import json
import csv
import math

def test_test_features_corrected_csv():
    path = "/home/user/test_features_corrected.csv"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r", newline='') as f:
        reader = list(csv.reader(f))

    assert len(reader) == 201, f"Expected 201 lines (1 header + 200 data rows) in {path}, got {len(reader)}."

    header = reader[0]
    assert header == ["user_id", "feature_a_norm", "feature_b_norm"], f"Unexpected CSV header: {header}"

    first_data_row = reader[1]
    assert first_data_row[0] == "u_800", f"Expected first data row user_id to be 'u_800', got {first_data_row[0]}"

    feature_a_norm = float(first_data_row[1])
    expected_u_800_norm = (800 - 399.5) / 230.94028832
    assert math.isclose(feature_a_norm, expected_u_800_norm, abs_tol=0.001), \
        f"Expected u_800 normalized feature_a to be ~{expected_u_800_norm:.4f}, got {feature_a_norm:.4f}."

def test_experiment_log_json():
    path = "/home/user/experiment_log.json"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} is not valid JSON."

    expected_values = {
        "train_feature_a_mean": 399.5000,
        "train_feature_a_std": 230.9403,
        "test_normalized_feature_a_mean": 2.1651,
        "test_normalized_feature_a_ci_lower": 2.1303,
        "test_normalized_feature_a_ci_upper": 2.1998
    }

    for key, expected in expected_values.items():
        assert key in log_data, f"Key '{key}' is missing from {path}."
        actual = float(log_data[key])
        assert math.isclose(actual, expected, abs_tol=0.001), \
            f"Expected '{key}' to be ~{expected}, got {actual}."